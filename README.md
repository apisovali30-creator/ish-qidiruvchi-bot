# 🧹👶 Oqila — Farrosh va Enaga Xizmatlari Platformasi (Telegram Mini App & Admin Panel)

Telegram ichida ishlaydigan zamonaviy **Telegram Mini App** va **Web Admin Dashboard**. Platforma diplomsiz xotin-qizlar uchun Farroshlik va Enagalik sohalarida ishonchli ish topish, mijozlar uchun esa sinovdan o'tgan, haqiqiy sharhlar va 5 yulduzli reytingga ega xodimlarni yollash imkonini beradi.

---

## 🌟 Asosiy Imkoniyatlar

1. **Faqat 2 ta xos soha (Diplom talab etilmaydi):**
   - 🧹 **Farrosh (Tozalik xodimi):** Xonadon, hovli, kottej va ta'mirdan keyingi tozalash.
   - 👶 **Enaga (Bolalar parvarishi):** Bolalarga qarash, tarbiya va parvarish.
2. **Yoshi va Yashash Tumani:**
   - Har bir nomzod yoshini (`🎂 36 yosh`) va yashash tumanini (`📍 Chilonzor tumani`) ko'rsatadi.
   - Toshkent shahrining 12 ta tumani va viloyatlar bo'yicha tezkor saralash.
3. **5 Yulduzli Baholash va Haqiqiy Sharhlar:**
   - Ishni bitirgach, ish beruvchi nomzodga 1 dan 5 gacha yulduzcha va matnli izoh qoldiradi.
   - O'rtacha reyting va sharhlar soni real vaqtda avtomatik hisoblanadi.
4. **Google Admin Panel (`/admin`):**
   - Faqat vakolatli Google hisob (`aliapisov11@gmail.com`) orqali kirish.
   - Anketalarni tasdiqlash, faol/nofaol qilish, buyurtmalarni boshqarish va noo'rin sharhlarni moderatsiya qilish.
5. **Telegram Bot Integratsiyasi:**
   - Yangi e'lon yoki sharh qoldirilganda Telegram orqali avtomatik bildirishnomalar.

---

## 🛠 Texnologiyalar

- **Backend:** Python 3.10+, FastAPI (Asinxron REST API va veb-server)
- **Telegram Bot:** aiogram 3 (Telegram bot boshqaruvi va bildirishnomalar)
- **Ma'lumotlar bazasi:** SQLite + aiosqlite (Asinxron relyatsion baza)
- **Frontend:** HTML5, CSS3 (Mobile-first, glassmorphism, zamonaviy gradient dizayn), Vanilla JavaScript, Telegram WebApp SDK
- **Admin Panel:** Google Identity Services (Google Sign-In) va xavfsiz boshqaruv paneli

---

## 📁 Loyiha Tuzilmasi

```
ish-qidiruvchi-bot/
├── config.py                 # Loyiha sozlamalari, kategoriyalar, tumanlar va admin
├── run.py                    # FastAPI server va aiogram botni parallel ishga tushiruvchi
├── seed_data.py              # Boshlang'ich sinov ma'lumotlari (nomzodlar va sharhlar)
├── requirements.txt          # Kerakli Python kutubxonalari
├── .env.example              # Namuna konfiguratsiya fayli
├── .gitignore                # Xavfsizlik: maxfiy fayllar va bazani himoyalash
├── database/
│   ├── __init__.py
│   └── db.py                 # SQLite relyatsion jadvallari, CRUD va statistika
├── bot/
│   ├── __init__.py
│   ├── bot_instance.py       # Bot dispatcher va bildirishnomalar yuborish
│   └── handlers/
│       ├── __init__.py
│       └── start.py          # /start va admin handlerlari
└── server/
    ├── __init__.py
    ├── app.py                # FastAPI REST API va Admin endpointlari
    └── static/               # Frontend fayllari
        ├── index.html        # Telegram WebApp foydalanuvchi sahifasi
        ├── style.css         # Olovrang gradient va glassmorphism stillar
        ├── app.js            # WebApp mantiqiy qismi
        ├── admin.html        # Google Admin Panel boshqaruv sahifasi
        ├── admin.css         # Admin dashboard stillari
        └── admin.js          # Admin boshqaruv mantiqi
```

---

## ⚡️ O'rnatish va Ishga Tushirish

### 1. Repozitoriyni klonlash va virtual muhit yaratish
```bash
git clone https://github.com/apisovali30-creator/ish-qidiruvchi-bot.git
cd ish-qidiruvchi-bot

python3 -m venv venv
source venv/bin/activate    # macOS / Linux
# Windows uchun: venv\Scripts\activate
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Konfiguratsiya (.env fayli)
`.env.example` dan nusxa olib `.env` faylini yarating:
```bash
cp .env.example .env
```
Va kerakli qiymatlarni kiriting:
```env
BOT_TOKEN=your_telegram_bot_token_here
WEBAPP_URL=https://your-domain.trycloudflare.com
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ADMIN_EMAIL=aliapisov11@gmail.com
ADMIN_SECRET_KEY=oqila_admin_secret_2026
```

### 4. Boshlang'ich ma'lumotlarni yuklash (ixtiyoriy)
```bash
python seed_data.py
```

### 5. Loyihani Ishga Tushirish
```bash
python run.py
```

- **Telegram WebApp:** Telegram bot ichida "Open" yoki `/start` bosilganda ochiladi.
- **Admin Panel:** Brauzerda `http://localhost:8000/admin` manzilida ochiladi (Faqat `aliapisov11@gmail.com` hisobi bilan kirish mumkin).
- **Swagger API Docs:** `http://localhost:8000/docs`

---

## 📄 Litsenziya
MIT License — erkin foydalanish va rivojlantirish uchun ochiq.
