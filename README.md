# 🍱 Kochi Kosen Shokudou Menu
> **ระบบจัดการเมนูโรงอาหารอัจฉริยะแบบอัตโนมัติ (AI-Powered Library)**

แอปพลิเคชันเว็บที่ช่วยให้นักเรียนและบุคลากรเข้าถึงเมนูโรงอาหารของ **Kochi NIT (Kosen)** ได้อย่างง่ายดาย โดยระบบจะดึงข้อมูลจากไฟล์ PDF ของโรงเรียนโดยอัตโนมัติ และใช้ AI ในการสกัดข้อมูลออกมาแสดงผลในรูปแบบที่สวยงามและทันสมัย

---

## 🌟 คุณสมบัติเด่น (Features)

*   **🔄 Automated Sync**: ระบบจะตรวจสอบและดึงไฟล์ PDF เมนูล่าสุดจากเว็บไซต์โรงเรียนโดยอัตโนมัติอ้างอิงตามสัปดาห์ปัจจุบัน
*   **🤖 AI Data Extraction**: ใช้เทคโนโลยี **Google Gemini (2.5 Flash / 2.0 Flash)** ในการอ่านและสกัดข้อมูลเมนูอาหารญี่ปุ่นจาก PDF/รูปภาพ แปลงเป็นข้อมูลดิจิทัลที่แม่นยำ
*   **📱 Modern & Responsive UI**: หน้าเมนูออกแบบด้วยสไตล์ Premium Glassmorphism รองรับการแสดงผลทุกหน้าจอ (Mobile-First)
*   **🖼️ Dynamic AI Food Previews**: แสดงรูปภาพเมนูอาหารจำลองที่สร้างโดย AI เพื่อเพิ่มความน่ารับประทาน
*   **⚙️ Powerful Admin Panel**: ระบบจัดการหลังบ้านที่สามารถอัปโหลดไฟล์เอง, แก้ไขข้อมูลด้วยมือ, หรือลบข้อมูลเพื่อ Sync ใหม่ได้
*   **💾 Multi-Database Support**: รองรับทั้ง **SQLite** (สำหรับการใช้งานส่วนตัว) และ **PostgreSQL** (สำหรับการ Deploy ขึ้น Production)

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

*   **Backend**: Python 3.12+ (Flask Framework)
*   **AI Engine**: Google Gemini API (Multimodal v1beta)
*   **Database**: SQLite (Local) / PostgreSQL (Production)
*   **Frontend**: Vanilla HTML5, Modern CSS, JavaScript (ES6)
*   **Deployment**: Render.com / Gunicorn WSGI

---

## 🚀 เริ่มต้นใช้งาน (Local Installation)

1.  **Clone Repository**
    ```bash
    git clone https://github.com/Kunpacito/KochiKosen_menu.git
    cd KochiKosen_menu
    ```

2.  **ติดตั้ง Library ที่จำเป็น**
    ```bash
    pip install -r requirements.txt
    ```

3.  **ตั้งค่า Environment Variables**
    *   สร้างไฟล์ `.env` ในโฟลเดอร์หลัก
    *   เพิ่ม API Key ของคุณ:
    ```env
    GEMINI_API_KEY=AIzaSy... (คีย์ของคุณจาก Google AI Studio)
    ```

4.  **รันแอปพลิเคชัน**
    ```bash
    python app.py
    ```
    เข้าใช้งานได้ที่: `http://127.0.0.1:5000`

---

## 🌐 การนำขึ้น Server (Deployment)

โปรเจกต์นี้ได้รับการกำหนดค่าให้พร้อมสำหรับ **Render.com**:

1.  **GitHub**: Push โค้ดขึ้น Repository ส่วนตัวของคุณ
2.  **Render Setup**: สร้าง "Web Service" ใหม่และเลือก Repo นี้
3.  **Environment**: เพิ่ม Variable ชื่อ `GEMINI_API_KEY` ในหน้า Settings
4.  **Database (Optional)**: หากต้องการความทนทานของข้อมูล แนะนำให้เชื่อมต่อกับ External PostgreSQL โดยเพิ่ม Variable `DATABASE_URL` (หากไม่ใส่ ระบบจะใช้ SQLite เป็นค่าเริ่มต้น)

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
KochiKosen_menu/
├── app.py              # ระบบหลักและการเชื่อมต่อ AI
├── requirements.txt    # รายการ Library ทั้งหมด
├── .env                # ไฟล์เก็บรหัสผ่าน (ห้ามแชร์!)
├── shokudou.db         # ไฟล์ฐานข้อมูล SQLite (Local)
├── static/             # ไฟล์รูปภาพและ CSS
├── templates/          # หน้าเว็บ (เมนู และ Admin)
└── README.md           # คู่มือการใช้งานนี้
```

---

## 📝 หมายเหตุ
- พัฒนาเพื่อช่วยให้นักเรียนสามารถเช็คเมนูอาหารได้สะดวกยิ่งขึ้น
- ข้อมูลเมนูอ้างอิงโดยตรงจากเว็บไซต์อย่างเป็นทางการของ Kochi NIT

---
**Developed by [Kunna]**  
*Part of the RoadToIntern Journey*
