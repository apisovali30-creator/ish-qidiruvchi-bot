# Loyihani Serverga (Bulutga) Deploy Qilish Qo'llanmasi

Ushbu qo'llanma orqali loyihani (FastAPI Mini App, Admin Panel va Telegram Bot) kompyuteringiz yopiq bo'lganda ham **24/7 uzluksiz** ishlashi uchun bepul yoki arzon bulutli serverlarga joylashtirishingiz mumkin.

GitHub Repozitoriya: **https://github.com/apisovali30-creator/ish-qidiruvchi-bot**

---

## 1-Usul: Render.com orqali bepul deploy qilish (Eng oson va tavsiya etiladi)

Render.com orqali GitHub repozitoriyangizni bevosita ulab, avtomatik deploy qilishingiz mumkin.

### Qadamlar:
1. [Render.com](https://render.com) saytiga kiring va GitHub orqali ro'yxatdan o'ting.
2. Bosh sahifada **"New +"** tugmasini bosing va **"Web Service"** ni tanlang.
3. **"Build and deploy from a Git repository"** ni tanlang va GitHub akkauntingizdan `apisovali30-creator/ish-qidiruvchi-bot` repozitoriyasini tanlang ("Connect" tugmasi).
4. Quyidagi sozlamalarni kiriting:
   - **Name:** `ish-qidiruvchi-bot`
   - **Region:** Frankfurt (EU Central) yoki Singapore (O'zbekistonga eng yaqini)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Instance Type:** `Free`
5. **Environment Variables (Muhit o'zgaruvchilari)** bo'limiga quyidagi kalitlarni qo'shing:
   - `BOT_TOKEN`: Sizning telegram bot tokeningiz (masalan, `9186651560:AAHGNLOrj7_09DnwdoZDoPbz35CD31R7Odc`)
   - `ADMIN_EMAIL`: `aliapisov11@gmail.com`
   - `ADMIN_SECRET_KEY`: Istalgan xavfsiz maxfiy kalit so'z
   - `WEBAPP_URL`: Render sizga beradigan HTTPS domen manzili (masalan: `https://ish-qidiruvchi-bot.onrender.com`)
6. **"Deploy Web Service"** tugmasini bosing.
7. Render bir necha daqiqada dasturni ishga tushiradi. Sayt manzilingiz tayyor bo'lgach (masalan `https://ish-qidiruvchi-bot.onrender.com`), Telegram botingiz avtomatik tarzda ushbu yangi manzilga ulanadi va notebookingiz o'chirilgan taqdirda ham bot va admin panel 24/7 ishlab turadi!

---

## 2-Usul: Railway.app orqali deploy qilish

1. [Railway.app](https://railway.app) saytiga kiring va GitHub bilan kiring.
2. **"New Project"** -> **"Deploy from GitHub repo"** ni tanlang.
3. `apisovali30-creator/ish-qidiruvchi-bot` repozitoriyasini tanlang.
4. **"Variables"** bo'limida quyidagilarni kiriting:
   - `BOT_TOKEN`
   - `ADMIN_EMAIL` (`aliapisov11@gmail.com`)
   - `ADMIN_SECRET_KEY`
5. Railway loyihani avtomatik quradi va bepul HTTPS domen beradi. Olingan domenni `WEBAPP_URL` ga yozing.

---

## 3-Usul: Docker orqali shaxsiy VPS (Ubuntu / Linux) serverda ishga tushirish

Agar sizda arzon VPS (masalan, Hetzner, DigitalOcean yoki Uztelecom VPS) bo'lsa:

```bash
# 1. Repozitoriyani yuklab olish
git clone https://github.com/apisovali30-creator/ish-qidiruvchi-bot.git
cd ish-qidiruvchi-bot

# 2. .env faylini yaratish
nano .env
# .env ichiga BOT_TOKEN, ADMIN_EMAIL, WEBAPP_URL ni yozing va saqlang

# 3. Docker bilan ishga tushirish
docker build -t ish-qidiruvchi-bot .
docker run -d --name ish-bot --restart always -p 8000:8000 --env-file .env ish-qidiruvchi-bot
```

---

## Foydali Havolalar va Xususiyatlar
- **Admin Panel:** `https://<sizning-domen>/admin` (Faqat `aliapisov11@gmail.com` Google hisobi orqali kiriladi)
- **Mini App:** `https://<sizning-domen>` (Telegram bot menyusi orqali ochiladi)
- **Xodimlar uchun "Bandman / Bo'shman" tugmasi:** Ishchilar o'z profillaridan turib 1 ta tugma orqali o'zlarini band yoki bo'sh deb belgilashlari mumkin.
