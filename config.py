import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

def reload_config():
    load_dotenv(BASE_DIR / ".env", override=True)

reload_config()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://pretty-eggs-build.loca.lt")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "8000")))

# Admin Panel sozlamalari (Faqat ruxsat berilgan Google hisob)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "aliapisov11@gmail.com")
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "oqila_admin_secret_2026")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
ADMIN_IDS = [5150570662]

def get_webapp_url() -> str:
    reload_config()
    return os.getenv("WEBAPP_URL", WEBAPP_URL)

DB_PATH = BASE_DIR / "platform.db"

CATEGORIES = [
    "Farroshlik (Tozalik)",
    "Enagalik (Parvarish)"
]

DISTRICTS = [
    "Chilonzor tumani",
    "Yunusobod tumani",
    "Mirzo Ulug'bek tumani",
    "Mirobod tumani",
    "Yashnobod tumani",
    "Yakkasaroy tumani",
    "Shayxontohur tumani",
    "Olmazor tumani",
    "Uchtepa tumani",
    "Sergeli tumani",
    "Yangihayot tumani",
    "Bektemir tumani",
    "Toshkent viloyati",
    "Samarqand shahri",
    "Farg'ona shahri",
    "Boshqa hudud"
]

WORK_TYPES = [
    "Kunlik (Bir martalik)",
    "Oylik (Doimiy)",
    "Soatbay",
    "Yotib ishlash (Sutkalik)"
]

REGIONS = DISTRICTS
