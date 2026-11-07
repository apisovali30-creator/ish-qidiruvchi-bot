import aiosqlite
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any
from config import DB_PATH

@asynccontextmanager
async def get_db():
    conn = await aiosqlite.connect(DB_PATH)
    conn.row_factory = aiosqlite.Row
    try:
        yield conn
    finally:
        await conn.close()

async def init_db() -> None:
    async with get_db() as db:
        # 1. Vacancies (Mijozlar buyurtmalari: Farrosh yoki Enaga kerak)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                profession TEXT NOT NULL DEFAULT 'Farrosh',
                district TEXT NOT NULL DEFAULT 'Chilonzor tumani',
                work_type TEXT NOT NULL DEFAULT 'Kunlik (Bir martalik)',
                salary TEXT NOT NULL,
                phone TEXT NOT NULL,
                telegram TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)

        # 2. Resumes (Enaga va Farrosh ayollar anketasi)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                profession TEXT NOT NULL DEFAULT 'Farrosh',
                age INTEGER NOT NULL DEFAULT 35,
                district TEXT NOT NULL DEFAULT 'Chilonzor tumani',
                work_type TEXT NOT NULL DEFAULT 'Kunlik (Bir martalik)',
                expected_salary TEXT,
                experience_years TEXT DEFAULT '2 yil tajriba',
                photo_url TEXT,
                phone TEXT NOT NULL,
                telegram TEXT,
                bio TEXT,
                avg_rating REAL DEFAULT 5.0,
                reviews_count INTEGER DEFAULT 0,
                is_busy INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)

        # 3. Reviews (Mijozlar qoldirgan baho va izohlar)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id INTEGER NOT NULL,
                author_name TEXT NOT NULL,
                author_user_id INTEGER,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (worker_id) REFERENCES resumes(id)
            )
        """)

        # Auto-migration for existing vacancies table columns
        async with db.execute("PRAGMA table_info(vacancies)") as cursor:
            vac_cols = [row[1] for row in await cursor.fetchall()]
            if "profession" not in vac_cols:
                await db.execute("ALTER TABLE vacancies ADD COLUMN profession TEXT DEFAULT 'Farrosh'")
            if "district" not in vac_cols:
                await db.execute("ALTER TABLE vacancies ADD COLUMN district TEXT DEFAULT 'Chilonzor tumani'")
            if "work_type" not in vac_cols:
                await db.execute("ALTER TABLE vacancies ADD COLUMN work_type TEXT DEFAULT 'Kunlik (Bir martalik)'")

        # Auto-migration for existing resumes table columns
        async with db.execute("PRAGMA table_info(resumes)") as cursor:
            res_cols = [row[1] for row in await cursor.fetchall()]
            if "profession" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN profession TEXT DEFAULT 'Farrosh'")
            if "age" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN age INTEGER DEFAULT 35")
            if "district" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN district TEXT DEFAULT 'Chilonzor tumani'")
            if "work_type" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN work_type TEXT DEFAULT 'Kunlik (Bir martalik)'")
            if "experience_years" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN experience_years TEXT DEFAULT '2 yil tajriba'")
            if "photo_url" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN photo_url TEXT")
            if "avg_rating" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN avg_rating REAL DEFAULT 5.0")
            if "reviews_count" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN reviews_count INTEGER DEFAULT 0")
            if "is_busy" not in res_cols:
                await db.execute("ALTER TABLE resumes ADD COLUMN is_busy INTEGER DEFAULT 0")

        # Indexes for speed
        await db.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_profession ON vacancies(profession)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_district ON vacancies(district)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_user ON vacancies(user_id)")

        await db.execute("CREATE INDEX IF NOT EXISTS idx_resumes_profession ON resumes(profession)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_resumes_district ON resumes(district)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_resumes_user ON resumes(user_id)")

        await db.execute("CREATE INDEX IF NOT EXISTS idx_reviews_worker ON reviews(worker_id)")

        await db.commit()

# --- Vacancies (Mijozlar e'lonlari / Buyurtmalari) ---

async def add_vacancy(
    user_id: int,
    title: str,
    profession: str,
    district: str,
    work_type: str,
    salary: str,
    phone: str,
    telegram: Optional[str] = None,
    description: Optional[str] = None
) -> int:
    async with get_db() as db:
        cursor = await db.execute("""
            INSERT INTO vacancies (user_id, title, company_name, category, region, profession, district, work_type, salary, phone, telegram, description, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            title.strip(),
            "Xonadon",
            profession.strip(),
            district.strip(),
            profession.strip(),
            district.strip(),
            work_type.strip(),
            salary.strip(),
            phone.strip(),
            telegram.strip() if telegram else None,
            description.strip() if description else None,
            "Ayol"
        ))
        await db.commit()
        return cursor.lastrowid

async def get_vacancies(
    profession: Optional[str] = None,
    district: Optional[str] = None,
    work_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    query = "SELECT * FROM vacancies WHERE is_active = 1"
    params: List[Any] = []

    if profession and profession != "Hammasi":
        query += " AND (profession LIKE ? OR title LIKE ?)"
        params.extend([f"%{profession}%", f"%{profession}%"])

    if district and district != "Hammasi":
        query += " AND district = ?"
        params.append(district)

    if work_type and work_type != "Hammasi":
        query += " AND work_type = ?"
        params.append(work_type)

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR district LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term, term])

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    async with get_db() as db:
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_vacancy_by_id(vacancy_id: int) -> Optional[Dict[str, Any]]:
    async with get_db() as db:
        async with db.execute("SELECT * FROM vacancies WHERE id = ? AND is_active = 1", (vacancy_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def delete_vacancy(vacancy_id: int, user_id: Optional[int] = None) -> bool:
    async with get_db() as db:
        if user_id is not None:
            cursor = await db.execute("UPDATE vacancies SET is_active = 0 WHERE id = ? AND user_id = ?", (vacancy_id, user_id))
        else:
            cursor = await db.execute("UPDATE vacancies SET is_active = 0 WHERE id = ?", (vacancy_id,))
        await db.commit()
        return cursor.rowcount > 0

# --- Resumes (Enaga va Farrosh Ayollar Katalogi) ---

async def add_resume(
    user_id: int,
    full_name: str,
    profession: str,
    age: int,
    district: str,
    work_type: str,
    expected_salary: Optional[str] = None,
    experience_years: str = "2 yil tajriba",
    photo_url: Optional[str] = None,
    phone: str = "",
    telegram: Optional[str] = None,
    bio: Optional[str] = None
) -> int:
    async with get_db() as db:
        cursor = await db.execute("""
            INSERT INTO resumes (user_id, full_name, profession, category, region, age, district, work_type, expected_salary, experience_years, photo_url, phone, telegram, bio, gender, avg_rating, reviews_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Ayol', 5.0, 0)
        """, (
            user_id,
            full_name.strip(),
            profession.strip(),
            profession.strip(),
            district.strip(),
            int(age),
            district.strip(),
            work_type.strip(),
            expected_salary.strip() if expected_salary else None,
            experience_years.strip() if experience_years else "1 yil tajriba",
            photo_url.strip() if photo_url else None,
            phone.strip(),
            telegram.strip() if telegram else None,
            bio.strip() if bio else None
        ))
        await db.commit()
        return cursor.lastrowid

async def get_resumes(
    profession: Optional[str] = None,
    district: Optional[str] = None,
    work_type: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    query = "SELECT * FROM resumes WHERE is_active = 1"
    params: List[Any] = []

    if profession and profession != "Hammasi":
        query += " AND (profession LIKE ?)"
        params.append(f"%{profession}%")

    if district and district != "Hammasi":
        query += " AND district = ?"
        params.append(district)

    if work_type and work_type != "Hammasi":
        query += " AND work_type = ?"
        params.append(work_type)

    if min_age is not None:
        query += " AND age >= ?"
        params.append(min_age)

    if max_age is not None:
        query += " AND age <= ?"
        params.append(max_age)

    if search:
        query += " AND (full_name LIKE ? OR bio LIKE ? OR district LIKE ?)"
        term = f"%{search.strip()}%"
        params.extend([term, term, term])

    query += " ORDER BY avg_rating DESC, id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    async with get_db() as db:
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_resume_by_id(resume_id: int) -> Optional[Dict[str, Any]]:
    async with get_db() as db:
        async with db.execute("SELECT * FROM resumes WHERE id = ? AND is_active = 1", (resume_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def delete_resume(resume_id: int, user_id: Optional[int] = None) -> bool:
    async with get_db() as db:
        if user_id is not None:
            cursor = await db.execute("UPDATE resumes SET is_active = 0 WHERE id = ? AND user_id = ?", (resume_id, user_id))
        else:
            cursor = await db.execute("UPDATE resumes SET is_active = 0 WHERE id = ?", (resume_id,))
        await db.commit()
        return cursor.rowcount > 0

async def set_resume_busy_status(resume_id: int, user_id: int, is_busy: int) -> bool:
    async with get_db() as db:
        cursor = await db.execute("""
            UPDATE resumes 
            SET is_busy = ? 
            WHERE id = ? AND user_id = ?
        """, (int(is_busy), resume_id, user_id))
        await db.commit()
        return cursor.rowcount > 0

# --- Reviews (Yulduzchalar va Izohlar) ---

async def add_review(
    worker_id: int,
    author_name: str,
    author_user_id: Optional[int],
    rating: int,
    comment: str
) -> Dict[str, Any]:
    rating = max(1, min(5, int(rating)))
    async with get_db() as db:
        cursor = await db.execute("""
            INSERT INTO reviews (worker_id, author_name, author_user_id, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (worker_id, author_name.strip(), author_user_id, rating, comment.strip()))
        review_id = cursor.lastrowid

        # Recalculate average rating & count for worker
        async with db.execute("""
            SELECT AVG(rating) as avg_score, COUNT(id) as total_count 
            FROM reviews WHERE worker_id = ?
        """, (worker_id,)) as calc_cursor:
            row = await calc_cursor.fetchone()
            avg_score = round(float(row["avg_score"] or 5.0), 1)
            total_count = int(row["total_count"] or 0)

        # Update resumes table with new rating stats
        await db.execute("""
            UPDATE resumes 
            SET avg_rating = ?, reviews_count = ? 
            WHERE id = ?
        """, (avg_score, total_count, worker_id))

        await db.commit()

        return {
            "id": review_id,
            "worker_id": worker_id,
            "avg_rating": avg_score,
            "reviews_count": total_count
        }

async def get_reviews_by_worker(worker_id: int) -> List[Dict[str, Any]]:
    async with get_db() as db:
        async with db.execute("""
            SELECT * FROM reviews 
            WHERE worker_id = ? 
            ORDER BY id DESC
        """, (worker_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

# --- User Posts ---

async def get_user_posts(user_id: int) -> Dict[str, Any]:
    async with get_db() as db:
        async with db.execute("SELECT * FROM vacancies WHERE user_id = ? AND is_active = 1 ORDER BY id DESC", (user_id,)) as c1:
            vacs = [dict(r) for r in await c1.fetchall()]

        async with db.execute("SELECT * FROM resumes WHERE user_id = ? AND is_active = 1 ORDER BY id DESC", (user_id,)) as c2:
            res = [dict(r) for r in await c2.fetchall()]

        return {"vacancies": vacs, "resumes": res}

# --- Admin Panel Funksiyalari ---

async def get_admin_stats() -> Dict[str, Any]:
    async with get_db() as db:
        # 1. Nomzodlar statistikasi
        async with db.execute("SELECT COUNT(*) as cnt FROM resumes") as c:
            total_resumes = (await c.fetchone())["cnt"]
        async with db.execute("SELECT COUNT(*) as cnt FROM resumes WHERE is_active = 1") as c:
            active_resumes = (await c.fetchone())["cnt"]
        async with db.execute("SELECT COUNT(*) as cnt FROM resumes WHERE profession LIKE '%Farrosh%'") as c:
            farrosh_count = (await c.fetchone())["cnt"]
        async with db.execute("SELECT COUNT(*) as cnt FROM resumes WHERE profession LIKE '%Enaga%'") as c:
            enaga_count = (await c.fetchone())["cnt"]

        # 2. Buyurtmalar statistikasi
        async with db.execute("SELECT COUNT(*) as cnt FROM vacancies") as c:
            total_vacancies = (await c.fetchone())["cnt"]
        async with db.execute("SELECT COUNT(*) as cnt FROM vacancies WHERE is_active = 1") as c:
            active_vacancies = (await c.fetchone())["cnt"]

        # 3. Sharhlar statistikasi
        async with db.execute("SELECT COUNT(*) as cnt, AVG(rating) as avg_score FROM reviews") as c:
            rev_row = await c.fetchone()
            total_reviews = rev_row["cnt"]
            avg_rating = round(float(rev_row["avg_score"] or 5.0), 1)

        return {
            "total_resumes": total_resumes,
            "active_resumes": active_resumes,
            "farrosh_count": farrosh_count,
            "enaga_count": enaga_count,
            "total_vacancies": total_vacancies,
            "active_vacancies": active_vacancies,
            "total_reviews": total_reviews,
            "avg_rating": avg_rating
        }

async def get_all_resumes_admin(
    search: Optional[str] = None,
    profession: Optional[str] = None,
    is_active: Optional[int] = None
) -> List[Dict[str, Any]]:
    async with get_db() as db:
        query = "SELECT * FROM resumes WHERE 1=1"
        params: List[Any] = []

        if profession:
            query += " AND profession LIKE ?"
            params.append(f"%{profession}%")
        if is_active is not None:
            query += " AND is_active = ?"
            params.append(is_active)
        if search:
            query += " AND (full_name LIKE ? OR district LIKE ? OR bio LIKE ? OR phone LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s, s])

        query += " ORDER BY id DESC"
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

async def toggle_resume_status(resume_id: int, is_active: Optional[int] = None) -> bool:
    async with get_db() as db:
        if is_active is None:
            await db.execute("UPDATE resumes SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END WHERE id = ?", (resume_id,))
        else:
            await db.execute("UPDATE resumes SET is_active = ? WHERE id = ?", (int(is_active), resume_id))
        await db.commit()
        return True

async def delete_resume(resume_id: int) -> bool:
    async with get_db() as db:
        # O'chirilgan ishchining sharhlarini ham tozalash
        await db.execute("DELETE FROM reviews WHERE worker_id = ?", (resume_id,))
        await db.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        await db.commit()
        return True

async def get_all_vacancies_admin(
    search: Optional[str] = None,
    is_active: Optional[int] = None
) -> List[Dict[str, Any]]:
    async with get_db() as db:
        query = "SELECT * FROM vacancies WHERE 1=1"
        params: List[Any] = []

        if is_active is not None:
            query += " AND is_active = ?"
            params.append(is_active)
        if search:
            query += " AND (title LIKE ? OR district LIKE ? OR description LIKE ? OR phone LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s, s])

        query += " ORDER BY id DESC"
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

async def toggle_vacancy_status(vacancy_id: int, is_active: Optional[int] = None) -> bool:
    async with get_db() as db:
        if is_active is None:
            await db.execute("UPDATE vacancies SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END WHERE id = ?", (vacancy_id,))
        else:
            await db.execute("UPDATE vacancies SET is_active = ? WHERE id = ?", (int(is_active), vacancy_id))
        await db.commit()
        return True

async def delete_vacancy(vacancy_id: int) -> bool:
    async with get_db() as db:
        await db.execute("DELETE FROM vacancies WHERE id = ?", (vacancy_id,))
        await db.commit()
        return True

async def get_all_reviews_admin() -> List[Dict[str, Any]]:
    async with get_db() as db:
        # Ishchining ismi bilan birga olish
        query = """
            SELECT r.*, res.full_name as worker_name, res.profession as worker_profession 
            FROM reviews r
            LEFT JOIN resumes res ON r.worker_id = res.id
            ORDER BY r.id DESC
        """
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

async def delete_review_admin(review_id: int) -> Optional[int]:
    async with get_db() as db:
        # Qaysi ishchiga tegishli ekanini bilish
        async with db.execute("SELECT worker_id FROM reviews WHERE id = ?", (review_id,)) as c:
            row = await c.fetchone()
            if not row:
                return None
            worker_id = row["worker_id"]

        # Sharhni o'chirish
        await db.execute("DELETE FROM reviews WHERE id = ?", (review_id,))

        # Ishchining umumiy reytingini va sharhlar sonini qayta hisoblash
        async with db.execute("""
            SELECT AVG(rating) as avg_score, COUNT(id) as total_count 
            FROM reviews WHERE worker_id = ?
        """, (worker_id,)) as calc_cursor:
            calc_row = await calc_cursor.fetchone()
            avg_score = round(float(calc_row["avg_score"] or 5.0), 1) if calc_row["total_count"] > 0 else 5.0
            total_count = int(calc_row["total_count"] or 0)

        await db.execute("""
            UPDATE resumes 
            SET avg_rating = ?, reviews_count = ? 
            WHERE id = ?
        """, (avg_score, total_count, worker_id))

        await db.commit()
        return worker_id

