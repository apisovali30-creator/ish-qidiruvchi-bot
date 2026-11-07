from pathlib import Path
from typing import Optional, List, Dict, Any
import secrets
import httpx
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import FileResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field

from config import (
    CATEGORIES, REGIONS, DISTRICTS, WORK_TYPES,
    ADMIN_EMAIL, ADMIN_SECRET_KEY, GOOGLE_CLIENT_ID
)
import database.db as db
from bot.bot_instance import notify_user

app = FastAPI(title="Farrosh va Enaga Xizmati Mini App API", version="3.0.0")

# Anti-cache middleware (Telegram WebApp eski keshni ushlab qolmasligi uchun)
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic modellari
class VacancyCreate(BaseModel):
    user_id: int
    title: str = Field(..., min_length=2, max_length=150)
    profession: str = Field(default="Farrosh", max_length=100)
    district: str = Field(default="Chilonzor tumani", max_length=100)
    work_type: str = Field(default="Kunlik (Bir martalik)", max_length=100)
    salary: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=7, max_length=30)
    telegram: Optional[str] = None
    description: Optional[str] = None
    company_name: Optional[str] = "Xonadon"
    category: Optional[str] = None
    region: Optional[str] = None
    gender: Optional[str] = "Ayol"

class ResumeCreate(BaseModel):
    user_id: int
    full_name: str = Field(..., min_length=2, max_length=150)
    profession: str = Field(default="Farrosh", max_length=100)
    age: int = Field(default=35, ge=18, le=80)
    district: str = Field(default="Chilonzor tumani", max_length=100)
    work_type: str = Field(default="Kunlik (Bir martalik)", max_length=100)
    expected_salary: Optional[str] = None
    experience_years: Optional[str] = "2 yil tajriba"
    photo_url: Optional[str] = None
    phone: str = Field(..., min_length=7, max_length=30)
    telegram: Optional[str] = None
    bio: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    gender: Optional[str] = "Ayol"

class ReviewCreate(BaseModel):
    worker_id: int
    author_name: str = Field(..., min_length=2, max_length=100)
    author_user_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=3, max_length=1000)

@app.on_event("startup")
async def on_startup():
    await db.init_db()

@app.get("/api/categories")
async def get_categories() -> List[str]:
    return CATEGORIES

@app.get("/api/districts")
async def get_districts() -> List[str]:
    return DISTRICTS

@app.get("/api/regions")
async def get_regions() -> List[str]:
    return REGIONS

@app.get("/api/work-types")
async def get_work_types() -> List[str]:
    return WORK_TYPES

# --- Vacancies Endpoints (Mijoz buyurtmalari: Enaga/Farrosh kerak) ---

@app.get("/api/vacancies")
async def list_vacancies(
    profession: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    work_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    selected_prof = profession or category
    selected_dist = district or region
    items = await db.get_vacancies(
        profession=selected_prof,
        district=selected_dist,
        work_type=work_type,
        search=search,
        limit=limit,
        offset=offset
    )
    return {"status": "ok", "data": items}

@app.get("/api/vacancies/{vacancy_id}")
async def get_vacancy(vacancy_id: int):
    item = await db.get_vacancy_by_id(vacancy_id)
    if not item:
        raise HTTPException(status_code=404, detail="E'lon topilmadi")
    return {"status": "ok", "data": item}

@app.post("/api/vacancies")
async def create_vacancy(payload: VacancyCreate):
    prof = payload.profession or payload.category or "Farrosh"
    dist = payload.district or payload.region or "Chilonzor tumani"
    wtype = payload.work_type or "Kunlik (Bir martalik)"

    vacancy_id = await db.add_vacancy(
        user_id=payload.user_id,
        title=payload.title,
        profession=prof,
        district=dist,
        work_type=wtype,
        salary=payload.salary,
        phone=payload.phone,
        telegram=payload.telegram,
        description=payload.description
    )

    notification_msg = (
        f"✅ <b>Buyurtmangiz muvaffaqiyatli e'lon qilindi!</b>\n\n"
        f"📌 <b>Kerakli xodim:</b> {prof}\n"
        f"📍 <b>Tuman:</b> {dist}\n"
        f"⏰ <b>Ish tartibi:</b> {wtype}\n"
        f"💰 <b>Taklif etilgan haq:</b> {payload.salary}\n\n"
        f"Buyurtmangiz platformadagi barcha xodimlarga ko'rinmoqda. Tez orada siz bilan bog'lanishadi! ✨"
    )
    await notify_user(payload.user_id, notification_msg)

    return {"status": "ok", "id": vacancy_id, "message": "Buyurtma muvaffaqiyatli yaratildi"}

# --- Resumes Endpoints (Enaga va Farrosh ayollar anketalari) ---

@app.get("/api/resumes")
async def list_resumes(
    profession: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    work_type: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    selected_prof = profession or category
    selected_dist = district or region
    items = await db.get_resumes(
        profession=selected_prof,
        district=selected_dist,
        work_type=work_type,
        min_age=min_age,
        max_age=max_age,
        search=search,
        limit=limit,
        offset=offset
    )
    return {"status": "ok", "data": items}

@app.get("/api/resumes/{resume_id}")
async def get_resume(resume_id: int):
    item = await db.get_resume_by_id(resume_id)
    if not item:
        raise HTTPException(status_code=404, detail="Nomzod anketasi topilmadi")
    return {"status": "ok", "data": item}

@app.post("/api/resumes")
async def create_resume(payload: ResumeCreate):
    prof = payload.profession or payload.category or "Farrosh"
    dist = payload.district or payload.region or "Chilonzor tumani"
    wtype = payload.work_type or "Kunlik (Bir martalik)"

    resume_id = await db.add_resume(
        user_id=payload.user_id,
        full_name=payload.full_name,
        profession=prof,
        age=payload.age,
        district=dist,
        work_type=wtype,
        expected_salary=payload.expected_salary,
        experience_years=payload.experience_years or "2 yil tajriba",
        photo_url=payload.photo_url,
        phone=payload.phone,
        telegram=payload.telegram,
        bio=payload.bio
    )

    salary_display = payload.expected_salary if payload.expected_salary else "Kelishilgan"
    notification_msg = (
        f"✅ <b>Anketangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
        f"👤 <b>Nomzod:</b> {payload.full_name}\n"
        f"💼 <b>Kasb:</b> {prof}\n"
        f"🎂 <b>Yoshi:</b> {payload.age} yoshda\n"
        f"📍 <b>Tuman:</b> {dist}\n"
        f"⏰ <b>Ish tartibi:</b> {wtype}\n"
        f"💰 <b>Kutilayotgan haq:</b> {salary_display}\n\n"
        f"Anketangiz mijozlar bazasiga kiritildi. Buyurtmalar tushganda siz bilan bog'lanishadi! 🎯"
    )
    await notify_user(payload.user_id, notification_msg)

    return {"status": "ok", "id": resume_id, "message": "Anketa muvaffaqiyatli yaratildi"}

# --- Reviews Endpoints (Baho va Izohlar) ---

@app.get("/api/workers/{worker_id}/reviews")
async def get_worker_reviews(worker_id: int):
    reviews = await db.get_reviews_by_worker(worker_id)
    return {"status": "ok", "data": reviews}

@app.post("/api/reviews")
async def create_review(payload: ReviewCreate):
    worker = await db.get_resume_by_id(payload.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Xodim topilmadi")

    res = await db.add_review(
        worker_id=payload.worker_id,
        author_name=payload.author_name,
        author_user_id=payload.author_user_id,
        rating=payload.rating,
        comment=payload.comment
    )

    # Agar xodimning Telegram user_id si bo'lsa, unga xushxabar yuboramiz
    if worker.get("user_id"):
        stars_str = "⭐" * payload.rating
        worker_msg = (
            f"🌟 <b>Sizga yangi mijoz izohi va bahosi qoldirildi!</b>\n\n"
            f"<b>Baho:</b> {stars_str} ({payload.rating}/5)\n"
            f"<b>Mijoz:</b> {payload.author_name}\n"
            f"<b>Izoh:</b> <i>\"{payload.comment}\"</i>\n\n"
            f"Umumiy reytingingiz: <b>⭐ {res['avg_rating']}</b> ({res['reviews_count']} ta izoh)"
        )
        await notify_user(worker["user_id"], worker_msg)

    return {"status": "ok", "data": res, "message": "Izohingiz muvaffaqiyatli qabul qilindi!"}

# --- User Posts Endpoints ---

@app.get("/api/my-posts")
async def my_posts(user_id: int = Query(...)):
    posts = await db.get_user_posts(user_id)
    return {"status": "ok", "data": posts}

@app.delete("/api/posts/{post_type}/{post_id}")
async def delete_post(post_type: str, post_id: int, user_id: Optional[int] = Query(None)):
    if post_type == "vacancy":
        success = await db.delete_vacancy(post_id, user_id)
    elif post_type == "resume":
        success = await db.delete_resume(post_id, user_id)
    else:
        raise HTTPException(status_code=400, detail="Noto'g'ri e'lon turi")

    if not success:
        raise HTTPException(status_code=404, detail="E'lon topilmadi yoki o'chirish huquqi yo'q")

    return {"status": "ok", "message": "E'lon muvaffaqiyatli o'chirildi"}

# --- User Profile Photo Endpoint ---
_avatar_cache: dict[int, bytes] = {}

@app.get("/api/user-avatar/{user_id}")
@app.head("/api/user-avatar/{user_id}")
async def get_user_avatar(user_id: int):
    """Foydalanuvchining Telegram profil rasmini (avatar) yuklab berish."""
    # Keshda mavjud bo'lsa darhol qaytarish
    if user_id in _avatar_cache:
        return Response(
            content=_avatar_cache[user_id],
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=86400"}
        )

    try:
        import httpx
        from bot.bot_instance import get_bot
        from config import BOT_TOKEN

        current_bot = get_bot()
        photos = await current_bot.get_user_profile_photos(user_id=user_id, limit=1)
        if photos.total_count > 0 and len(photos.photos[0]) > 0:
            # 320x320 yoki eng mos o'lchamdagi rasmni tanlash
            selected = photos.photos[0][1] if len(photos.photos[0]) > 1 else photos.photos[0][0]
            tg_file = await current_bot.get_file(selected.file_id)
            if tg_file.file_path:
                download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(download_url)
                    if resp.status_code == 200 and resp.content:
                        _avatar_cache[user_id] = resp.content
                        return Response(
                            content=resp.content,
                            media_type="image/jpeg",
                            headers={"Cache-Control": "public, max-age=86400"}
                        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Foydalanuvchi avatari yuklashda xatolik ({user_id}): {e}")

    raise HTTPException(status_code=404, detail="Avatar topilmadi")

# --- Admin Autentifikatsiya va Sessiyalar ---
_admin_sessions: Dict[str, Dict[str, Any]] = {}

class AdminLoginRequest(BaseModel):
    credential: Optional[str] = None  # Google ID token (GIS)
    email: Optional[str] = None
    secret_key: Optional[str] = None

security_scheme = HTTPBearer(auto_error=False)

async def get_current_admin(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)):
    if not credentials or credentials.credentials not in _admin_sessions:
        raise HTTPException(status_code=401, detail="Sessiya mavjud emas yoki muddati tugagan. Iltimos, qayta kiring.")
    return _admin_sessions[credentials.credentials]

# Frontend Statik fayllari
STATIC_DIR = Path(__file__).resolve().parent / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/admin")
@app.get("/admin/")
async def serve_admin_page():
    admin_file = STATIC_DIR / "admin.html"
    if admin_file.exists():
        return FileResponse(str(admin_file))
    raise HTTPException(status_code=404, detail="Admin panel fayli topilmadi")

@app.get("/api/admin/config")
async def get_admin_client_config():
    """Frontend Google Sign-In uchun Client ID va ruxsat berilgan email"""
    return {
        "admin_email": ADMIN_EMAIL,
        "google_client_id": GOOGLE_CLIENT_ID
    }

@app.post("/api/admin/login")
async def admin_login(data: AdminLoginRequest):
    admin_email_target = ADMIN_EMAIL.strip().lower()
    user_name = "Ali (Admin)"
    user_picture = None

    # 1. Google ID token orqali kirish
    if data.credential:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={data.credential}")
                if res.status_code != 200:
                    raise HTTPException(status_code=401, detail="Google tokeni yaroqsiz")
                token_data = res.json()
                verified_email = token_data.get("email", "").strip().lower()
                user_name = token_data.get("name", "Ali (Admin)")
                user_picture = token_data.get("picture")

                if verified_email != admin_email_target:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Kirish taqiqlangan! '{verified_email}' hisobi admin emas. Faqat {ADMIN_EMAIL} admin hisoblanadi."
                    )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Google tekshiruvida xatolik: {str(e)}")

    # 2. To'g'ridan-to'g'ri maxfiy kalit va email orqali kirish
    elif data.email and data.secret_key:
        input_email = data.email.strip().lower()
        if input_email != admin_email_target:
            raise HTTPException(
                status_code=403,
                detail=f"Kirish taqiqlangan! Faqat {ADMIN_EMAIL} admin hisoblanadi."
            )
        if data.secret_key != ADMIN_SECRET_KEY:
            raise HTTPException(status_code=401, detail="Noto'g'ri maxfiy kalit!")
    else:
        raise HTTPException(status_code=400, detail="Google tokeni yoki email va maxfiy kalit talab qilinadi")

    # Yangi xavfsiz sessiya tokeni yaratish
    session_token = secrets.token_hex(32)
    _admin_sessions[session_token] = {
        "email": ADMIN_EMAIL,
        "name": user_name,
        "picture": user_picture,
        "role": "Super Admin"
    }

    return {
        "status": "ok",
        "token": session_token,
        "admin": _admin_sessions[session_token]
    }

@app.post("/api/admin/logout")
async def admin_logout(admin: Dict[str, Any] = Depends(get_current_admin), credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)):
    if credentials and credentials.credentials in _admin_sessions:
        del _admin_sessions[credentials.credentials]
    return {"status": "ok", "message": "Tizimdan chiqildi"}

@app.get("/api/admin/me")
async def admin_me(admin: Dict[str, Any] = Depends(get_current_admin)):
    return {"status": "ok", "admin": admin}

@app.get("/api/admin/stats")
async def admin_stats(admin: Dict[str, Any] = Depends(get_current_admin)):
    stats = await db.get_admin_stats()
    return {"status": "ok", "stats": stats}

@app.get("/api/admin/resumes")
async def admin_get_resumes(
    search: Optional[str] = None,
    profession: Optional[str] = None,
    is_active: Optional[int] = None,
    admin: Dict[str, Any] = Depends(get_current_admin)
):
    items = await db.get_all_resumes_admin(search=search, profession=profession, is_active=is_active)
    return {"status": "ok", "data": items, "count": len(items)}

@app.patch("/api/admin/resumes/{item_id}/toggle")
async def admin_toggle_resume(item_id: int, admin: Dict[str, Any] = Depends(get_current_admin)):
    await db.toggle_resume_status(item_id)
    return {"status": "ok", "message": f"Anketa #{item_id} holati yangilandi"}

@app.delete("/api/admin/resumes/{item_id}")
async def admin_delete_resume(item_id: int, admin: Dict[str, Any] = Depends(get_current_admin)):
    await db.delete_resume(item_id)
    return {"status": "ok", "message": f"Anketa #{item_id} o'chirildi"}

@app.get("/api/admin/vacancies")
async def admin_get_vacancies(
    search: Optional[str] = None,
    is_active: Optional[int] = None,
    admin: Dict[str, Any] = Depends(get_current_admin)
):
    items = await db.get_all_vacancies_admin(search=search, is_active=is_active)
    return {"status": "ok", "data": items, "count": len(items)}

@app.patch("/api/admin/vacancies/{item_id}/toggle")
async def admin_toggle_vacancy(item_id: int, admin: Dict[str, Any] = Depends(get_current_admin)):
    await db.toggle_vacancy_status(item_id)
    return {"status": "ok", "message": f"Buyurtma #{item_id} holati yangilandi"}

@app.delete("/api/admin/vacancies/{item_id}")
async def admin_delete_vacancy(item_id: int, admin: Dict[str, Any] = Depends(get_current_admin)):
    await db.delete_vacancy(item_id)
    return {"status": "ok", "message": f"Buyurtma #{item_id} o'chirildi"}

@app.get("/api/admin/reviews")
async def admin_get_reviews(admin: Dict[str, Any] = Depends(get_current_admin)):
    items = await db.get_all_reviews_admin()
    return {"status": "ok", "data": items, "count": len(items)}

@app.delete("/api/admin/reviews/{item_id}")
async def admin_delete_review(item_id: int, admin: Dict[str, Any] = Depends(get_current_admin)):
    worker_id = await db.delete_review_admin(item_id)
    if not worker_id:
        raise HTTPException(status_code=404, detail="Sharh topilmadi")
    return {"status": "ok", "message": f"Sharh #{item_id} o'chirildi va ishchining reytingi qayta hisoblandi"}

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

