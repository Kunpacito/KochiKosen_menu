import json
try:
    with open('last_json_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        text = data['candidates'][0]['content']['parts'][0]['text']
        print("Text length:", len(text))
        print("First 200 chars:", text[:200])
        print("Last 200 chars:", text[-200:])
        
        # Check for unterminated strings
        try:
            json.loads(text)
            print("JSON is valid!")
        except Exception as e:
            print("JSON is INVALID:", e)
            # Find the line/char from error
            import re
            m = re.search(r'line (\d+) column (\d+)', str(e))
            if m:
                line_no = int(m.group(1))
                col_no = int(m.group(2))
                lines = text.splitlines()
                if line_no <= len(lines):
                    print(f"Problem at line {line_no}:")
                    print(lines[line_no-1])
                    print(" " * (col_no-1) + "^")
except Exception as e:
    print("Error reading or parsing raw json:", e)
