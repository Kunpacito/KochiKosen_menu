# 🍱 Shokudou Menu (ระบบจัดการเมนูโรงอาหารอัจฉริยะ)

ระบบจัดการและแสดงผลเมนูอาหารรายสัปดาห์แบบอัตโนมัติ สำหรับโรงอาหาร Kochi NIT (Kosen) โดยใช้พลังของ AI (Gemini API) ในการอ่านไฟล์ PDF/รูปภาพ และแสดงผลผ่านหน้าเว็บที่สวยงามและใช้งานง่าย

---

## 🌟 คุณสมบัติเด่น (Features)

*   **🔄 Auto-Sync**: ดึงไฟล์ PDF เมนูจากเว็บไซต์โรงอาหารโดยอัตโนมัติอ้างอิงตามสัปดาห์ปัจจุบัน
*   **🤖 AI Parser**: ใช้ **Gemini 1.5 Flash** ในการสกัดข้อมูลเมนูอาหารญี่ปุ่นจาก PDF เป็น JSON อย่างแม่นยำ
*   **📅 Weekly Dashboard**: หน้าเมนูสำหรับนักเรียนที่รองรับ Dark Mode และ Responsive (มือถือดูง่าย)
*   **🖼️ AI Food Images**: สร้างรูปภาพจำลองเมนูอาหารให้น่ารับประทานโดยใช้ Pollinations AI
*   **🛡️ Admin Panel**: ระบบจัดการหลังบ้านที่ครบครัน (Upload, URL Fetch, Manual Edit, Delete)
*   **🔒 Security First**: จัดเก็บ API Key ผ่าน Environment Variables ป้องกันรหัสหลุดสู่สาธารณะ

---

## 🛠️ เทคโนโลยี (Tech Stack)

*   **Backend**: Python (Flask)
*   **Database**: SQLite3
*   **AI Engine**: Google Gemini 1.5 Flash (API)
*   **Deployment**: Render.com / Gunicorn
*   **Frontend**: Vanilla HTML5, Modern CSS (Glassmorphism), JavaScript (ES6)

---

## 🚀 การติดตั้งและเริ่มใช้งาน (Local Installation)

1.  **Clone Repository**
    ```bash
    git clone https://github.com/Kunpacito/KochiKosen_menu.git
    cd KochiKosen_menu
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**
    *   สร้างไฟล์ `.env` ในโฟลเดอร์หลัก
    *   เพิ่ม API Key ของคุณ:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Run Application**
    ```bash
    python app.py
    ```
    เข้าใช้งานที่: `http://localhost:5000`

---

## 🌐 การนำขึ้น Server (Deployment to Render)

โปรเจคนี้พร้อมสำหรับการ Deploy บน Render.com ทันที:
1.  **Push โค้ดขึ้น GitHub** (ตั้งค่า Repository เป็น **Private**)
2.  **เชื่อมต่อกับ Render**: สร้าง Web Service ใหม่และเลือก Repo นี้
3.  **ตั้งค่า Environment**: ในหน้า Dashboard ของ Render ให้เพิ่ม Variable ชื่อ `GEMINI_API_KEY`
4.  **Build & Start**: 
    *   Build: `pip install -r requirements.txt`
    *   Start: `gunicorn app:app`

---

## 📁 โครงสร้างโปรเจค (Project Structure)

```text
shokudou_menu/
├── app.py              # Backend Logic & AI Integration
├── .env                # เก็บ API Key (ห้ามอัปโหลด!)
├── .gitignore          # ระบุไฟล์ที่ไม่ต้องการนำขึ้น GitHub
├── Procfile            # คำสั่งสำหรับรันบน Server (Render)
├── requirements.txt    # รายการ Library ที่ต้องใช้
├── templates/          # HTML Templates (menu.html, admin.html)
├── static/             # Static Assets & Uploads
└── README.md           # คู่มือการใช้งาน
```

---

## 📝 หมายเหตุ
- ข้อมูลใน SQLite (`shokudou.db`) จะหายไปหากใช้ Render แผนฟรี (Ephemeral Storage) แต่ระบบสามารถ Sync ข้อมูลใหม่ได้เสมอ
- พัฒนาต่อยอดจากโปรเจค **RoadToIntern** โดย [Kunna]
