from flask import Flask, render_template, request, jsonify
import sqlite3, os, json, base64, re, requests
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# -------------------------------------------------------------------------
# GEMINI API Key (Loaded from .env)
# -------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

BASE_DIR   = os.path.dirname(__file__)
DB_PATH    = os.path.join(BASE_DIR, 'shokudou.db')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf'}

# -------------------------------------------------------------------------
# Database
# -------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS menu_data (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                date       TEXT    NOT NULL,
                meal_type  TEXT    NOT NULL,
                main_dish  TEXT    DEFAULT '',
                items      TEXT    DEFAULT '[]',
                kcal       TEXT    DEFAULT '',
                updated_at TEXT    DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, meal_type)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sync_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_monday TEXT,
                status TEXT,
                error_msg TEXT,
                attempted_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------
def get_monday(dt):
    # weekday() returns 0 for Monday
    return (dt - timedelta(days=dt.weekday())).date()

def parse_with_gemini(mime_type, data_b64):
    prompt = (
        "You are an expert data extractor. Extract the menu from this Japanese cafeteria (食堂) weekly menu image or pdf.\n"
        "Return ONLY a valid JSON object matching the exact format below, without any markdown formatting.\n"
        '{"days":[{"date":"2024-01-01",'
        '"朝食":{"main":"ライス / パン","items":["Item 1", "Item 2"],"kcal":"1100kcal"},'
        '"昼食":{"main":"","items":["Dish A"],"kcal":"900kcal"},'
        '"夕食":{"main":"","items":["Dish B"],"kcal":"950kcal"}}]}\n'
        "CRITICAL RULES:\n"
        "1. Columns represent days (月〜日). Extract dates from headers.\n"
        "2. 朝食=morning, 昼食=lunch, 夕食=dinner.\n"
        "3. Keep descriptions EXTREMELY short and concise. DO NOT write full sentences.\n"
        "4. DO NOT REPEAT ANY TEXT. If you find yourself repeating, stop immediately.\n"
        "5. IMPORTANT: Extract the original text in JAPANESE. Do not translate to other languages."
    )

    body = {
        'systemInstruction': {'parts': [{'text': 'You are a Japanese cafeteria menu parser. Always return ONLY valid JSON matching the requested schema.'}]},
        'contents': [{'parts': [
            {'text': prompt},
            {'inlineData': {'mimeType': mime_type, 'data': data_b64}}
        ]}],
        'generationConfig': {
            'temperature': 0.1, 
            'maxOutputTokens': 32768,
            'responseMimeType': 'application/json'
        }
    }

    # Using v1beta with Gemini 3 Flash (latest available in 2026)
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}'
           
    session = requests.Session()
    resp = session.post(url, json=body, timeout=60)
    
    # Detailed logging for debugging
    with open(os.path.join(BASE_DIR, 'debug_api.txt'), 'a', encoding='utf-8') as f:
        f.write(f"--- {datetime.now()} ---\nStatus: {resp.status_code}\nResponse: {resp.text}\n---\n")
    
    if resp.status_code == 429:
        raise Exception("AI Rate Limit: โควต้าใช้งาน AI เต็มชั่วคราว (Gemini API 429) กรุณาลองใหม่ในภายหลังหรือเปลี่ยน API Key")
    
    resp.raise_for_status()
    text = resp.json()['candidates'][0]['content']['parts'][0]['text']
    
    cleaned_text = text.strip()
    if cleaned_text.startswith('```json'):
        cleaned_text = cleaned_text[7:]
    elif cleaned_text.startswith('```'):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith('```'):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        # Fallback: if JSON is broken, try to find the first { and last }
        start = cleaned_text.find('{')
        end = cleaned_text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(cleaned_text[start:end+1])
            except:
                pass
        raise Exception(f"JSON Parsing Error: {str(e)} | Text Preview: {cleaned_text[:500]}...")

def sync_menu_from_school():
    """Calculates current week's Monday and fetches PDF if missing from DB."""
    now = datetime.now()
    monday = get_monday(now)
    monday_str = monday.strftime("%Y-%m-%d")
    
    with get_db() as conn:
        # 1. Check if data already exists
        row = conn.execute('SELECT 1 FROM menu_data WHERE date = ? LIMIT 1', (monday_str,)).fetchone()
        if row: return

        # 2. Check persistent cooldown (don't retry more than once every 1 hour if it failed)
        last_log = conn.execute('''
            SELECT attempted_at FROM sync_logs 
            WHERE date_monday = ? AND status = 'error' 
            ORDER BY attempted_at DESC LIMIT 1
        ''', (monday_str,)).fetchone()
        
        if last_log:
            last_time = datetime.strptime(last_log['attempted_at'], '%Y-%m-%d %H:%M:%S')
            if (now - last_time).total_seconds() < 3600: # 1 hour cooldown
                return

    # 3. Proceed with sync
    url_date = monday.strftime("%Y%m%d")
    pdf_url = f"https://www.kochi-ct.ac.jp/files/uploads/kondate{url_date}.pdf"
    
    try:
        resp = requests.get(pdf_url, timeout=30)
        if resp.status_code == 200:
            pdf_b64 = base64.b64encode(resp.content).decode()
            parsed = parse_with_gemini('application/pdf', pdf_b64)
            
            if parsed and 'days' in parsed:
                with get_db() as conn:
                    for day in parsed['days']:
                        d = day.get('date')
                        if not d: continue
                        for meal_type in ['朝食', '昼食', '夕食']:
                            info = day.get(meal_type)
                            if info:
                                items_json = json.dumps(info.get('items', []), ensure_ascii=False)
                                conn.execute('''
                                    INSERT INTO menu_data (date, meal_type, main_dish, items, kcal, updated_at)
                                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                                    ON CONFLICT(date, meal_type) DO UPDATE SET
                                        main_dish  = excluded.main_dish,
                                        items      = excluded.items,
                                        kcal       = excluded.kcal,
                                        updated_at = CURRENT_TIMESTAMP
                                ''', (d, meal_type, info.get('main', ''), items_json, info.get('kcal', '')))
                    
                    conn.execute('INSERT INTO sync_logs (date_monday, status) VALUES (?, ?)', (monday_str, 'success'))
                    conn.commit()
                    print(f"Auto-sync successful for {monday_str}")
        else:
            with get_db() as conn:
                conn.execute('INSERT INTO sync_logs (date_monday, status, error_msg) VALUES (?, ?, ?)', 
                             (monday_str, 'error', f'HTTP {resp.status_code}'))
                conn.commit()
    except Exception as e:
        print(f"Auto-sync failed for {pdf_url}: {e}")
        with get_db() as conn:
            conn.execute('INSERT INTO sync_logs (date_monday, status, error_msg) VALUES (?, ?, ?)', 
                         (monday_str, 'error', str(e)))
            conn.commit()

# -------------------------------------------------------------------------
# Pages
# -------------------------------------------------------------------------
@app.route('/')
def menu_view():
    return render_template('menu.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# -------------------------------------------------------------------------
# API
# -------------------------------------------------------------------------
@app.route('/api/menu')
def api_get_menu():
    # Attempt auto-fetch if current week is missing
    sync_menu_from_school()

    with get_db() as conn:
        rows = conn.execute(
            'SELECT date, meal_type, main_dish, items, kcal FROM menu_data ORDER BY date'
        ).fetchall()
    result = {}
    for row in rows:
        d = row['date']
        if d not in result:
            result[d] = {}
        result[d][row['meal_type']] = {
            'main':  row['main_dish'],
            'items': json.loads(row['items']),
            'kcal':  row['kcal'],
        }
    return jsonify(result)

@app.route('/api/menu/save', methods=['POST'])
def api_save_menu():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    saved = 0
    with get_db() as conn:
        for date, meals in data.items():
            for meal_type, info in meals.items():
                items_json = json.dumps(info.get('items', []), ensure_ascii=False)
                conn.execute('''
                    INSERT INTO menu_data (date, meal_type, main_dish, items, kcal, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(date, meal_type) DO UPDATE SET
                        main_dish  = excluded.main_dish,
                        items      = excluded.items,
                        kcal       = excluded.kcal,
                        updated_at = CURRENT_TIMESTAMP
                ''', (date, meal_type,
                      info.get('main', ''), items_json, info.get('kcal', '')))
                saved += 1
        conn.commit()
    return jsonify({'success': True, 'saved': saved})

@app.route('/api/menu/delete-day', methods=['POST'])
def api_delete_day():
    date = request.get_json().get('date')
    if not date:
        return jsonify({'error': 'No date provided'}), 400
    with get_db() as conn:
        conn.execute('DELETE FROM menu_data WHERE date = ?', (date,))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/menu/delete-all', methods=['POST'])
def api_delete_all():
    with get_db() as conn:
        conn.execute('DELETE FROM menu_data')
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/parse-image', methods=['POST'])
def api_parse_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(f"menu_{ts}_{file.filename}")
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    with open(file_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()

    mime = file.content_type or 'image/jpeg'

    try:
        parsed = parse_with_gemini(mime, img_b64)
        return jsonify({
            'success': True,
            'data': parsed,
            'file_url': f'/static/uploads/{filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch-url-menu', methods=['POST'])
def api_fetch_url_menu():
    date_str = request.get_json().get('date')
    if not date_str:
        return jsonify({'error': 'No date provided'}), 400
        
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        url_date = dt.strftime("%Y%m%d")
        pdf_url = f"https://www.kochi-ct.ac.jp/files/uploads/kondate{url_date}.pdf"
        
        resp = requests.get(pdf_url, timeout=30)
        if resp.status_code == 404:
            return jsonify({'error': f'ไม่พบไฟล์ PDF บนเว็บไซต์ (URL: {pdf_url})'}), 404
        resp.raise_for_status()
        
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"kondate_{url_date}_{ts}.pdf"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, 'wb') as f:
            f.write(resp.content)
            
        pdf_b64 = base64.b64encode(resp.content).decode()
        
        parsed = parse_with_gemini('application/pdf', pdf_b64)
        return jsonify({
            'success': True,
            'data': parsed,
            'file_url': f'/static/uploads/{filename}',
            'is_pdf': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
