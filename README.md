# 🍱 Shokudou Menu (ระบบจัดการเมนูโรงอาหาร)

ระบบจัดการและแสดงผลเมนูอาหารรายสัปดาห์แบบอัตโนมัติ โดยใช้ AI (Gemini API) ในการดึงข้อมูลจากรูปภาพหรือไฟล์ PDF ของโรงอาหาร Kochi NIT (Kosen) เพื่อความสะดวกในการตรวจสอบเมนูอาหารล่วงหน้า

---

## 🌟 คุณสมบัติเด่น (Features)

*   **🔄 Auto-Sync**: ระบบคำนวณวันจันทร์ของสัปดาห์ปัจจุบัน และดึงไฟล์ PDF เมนูจากเว็บไซต์โรงอาหารโดยอัตโนมัติ
*   **🤖 AI Menu Parsing**: ใช้ **Gemini API (Flash Preview)** ในการอ่านและสกัดข้อมูลจากรูปภาพเมนูหรือไฟล์ PDF แปลงเป็นข้อมูล JSON ที่พร้อมใช้งาน
*   **📅 Weekly Dashboard**: หน้าแสดงผลเมนูอาหารที่สวยงาม แบ่งตามวัน (จันทร์-อาทิตย์) และมื้ออาหาร (เช้า, กลางวัน, เย็น)
*   **🛡️ Admin Management**: ระบบหลังบ้านสำหรับ:
    *   อัปโหลดรูปภาพเมนูใหม่
    *   ดึงข้อมูลจาก URL ของโรงอาหารโดยตรง
    *   แก้ไขข้อมูลเมนูอาหารด้วยตนเอง
    *   จัดการลบข้อมูลรายวันหรือลบทั้งหมด
*   **📊 Nutrition Info**: แสดงข้อมูลแคลอรี่ (kcal) และรายการอาหารย่อย (Side dishes) ในแต่ละมื้อ

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

*   **Backend**: Python (Flask)
*   **Database**: SQLite3 (มีความเบาและไม่ต้องตั้งค่าเซิร์ฟเวอร์แยก)
*   **AI Integration**: Google Gemini 3 Flash (v1beta)
*   **Frontend**: HTML5, Vanilla CSS (Modern Design), JavaScript (Fetch API)

---

## 🚀 การติดตั้งและเริ่มใช้งาน (Getting Started)

### 1. ติดตั้งสิ่งที่จำเป็น
ตรวจสอบว่าคุณมี Python 3.8 ขึ้นไปติดตั้งอยู่ในเครื่อง

```bash
# ตรวจสอบเวอร์ชัน Python
python --version
```

### 2. ติดตั้ง Dependencies
ติดตั้งไลบรารีที่จำเป็นผ่าน pip:

```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า API Key
เปิดไฟล์ `app.py` และระบุ **Gemini API Key** ของคุณในส่วนหัวของไฟล์:

```python
# app.py
GEMINI_API_KEY = 'AIzaSy...' # ใส่ API Key ของคุณที่นี่
```

### 4. รันแอปพลิเคชัน
เริ่มการทำงานของเซิร์ฟเวอร์:

```bash
python app.py
```

เข้าใช้งานผ่านเบราว์เซอร์ที่: [http://localhost:5000](http://localhost:5000)

---

## 📁 โครงสร้างโปรเจค (Project Structure)

```text
shokudou_menu/
├── app.py              # ไฟล์หลักควบคุม Server Logic และ AI Integration
├── shokudou.db         # ฐานข้อมูล SQLite (สร้างให้อัตโนมัติ)
├── requirements.txt    # รายการ Library ที่ต้องใช้
├── templates/          # ไฟล์ HTML Templates
│   ├── menu.html       # หน้า Dashboard สำหรับผู้ใช้
│   └── admin.html      # หน้าจัดการระบบสำหรับ Admin
├── static/             # ไฟล์ Static Assets
│   ├── css/            # ไฟล์สไตล์การตกแต่ง
│   └── uploads/        # โฟลเดอร์เก็บไฟล์ PDF/รูปภาพ ที่อัปโหลด
└── README.md           # ไฟล์เอกสารแนะนำโปรเจค
```

---

## 📝 หมายเหตุ
- ระบบถูกออกแบบมาเพื่อรองรับรูปแบบไฟล์ PDF ของโรงอาหาร Kochi NIT (Kosen) เป็นหลัก
- ในการใช้งานฟีเจอร์ AI จำเป็นต้องมีการเชื่อมต่ออินเทอร์เน็ตเพื่อส่งข้อมูลไปยัง Gemini API

---
พัฒนาโดย [Kunna] - ส่วนหนึ่งของโปรเจค RoadToIntern
