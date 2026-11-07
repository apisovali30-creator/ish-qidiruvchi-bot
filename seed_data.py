import asyncio
from pathlib import Path
import database.db as db

SAMPLE_WORKERS = [
    {
        "user_id": 88801,
        "full_name": "Dilnoza opa Karimova",
        "profession": "Farrosh",
        "age": 38,
        "district": "Chilonzor tumani",
        "work_type": "Kunlik (Bir martalik)",
        "expected_salary": "350 000 so'm / kuniga",
        "experience_years": "5 yil tajriba",
        "phone": "+998 90 345 12 89",
        "telegram": "@dilnoza_tozalik",
        "bio": "Uylarni, kottejlarni va ta'mirdan chiqqan xonadonlarni boshdan-oyoq chinnidek tozalayman. Deraza yuvish, oshxona yog'larini ketkazish va mebellarni ehtiyotlab tozalash. Halol va chaqqonman.",
        "reviews": [
            {
                "author_name": "Aziza Yusupova",
                "author_user_id": 101,
                "rating": 5,
                "comment": "Dilnoza opaga katta rahmat! 4 xonali uyimizni 5 soatda xuddi yangidek tozalab berdilar, derazalarda birorta dog' qolmadi. Juda chaqqon va halol ayol ekanlar."
            },
            {
                "author_name": "Jamshidbek",
                "author_user_id": 102,
                "rating": 5,
                "comment": "Oshxonani shunday tozalab berdilar, yangi kelyapmiz deb o'ylaysiz. Doimiy chaqirib turamiz endi."
            },
            {
                "author_name": "Moxira",
                "author_user_id": 103,
                "rating": 5,
                "comment": "Halolligi va tartibliligi juda yoqdi. Ishini chin dildan qiladigan inson ekanlar."
            }
        ]
    },
    {
        "user_id": 88802,
        "full_name": "Nilufar opa Xolmirzayeva",
        "profession": "Enaga",
        "age": 44,
        "district": "Yunusobod tumani",
        "work_type": "Oylik (Doimiy)",
        "expected_salary": "4 500 000 so'm / oyiga",
        "experience_years": "8 yil tajriba",
        "phone": "+998 93 512 67 43",
        "telegram": "@nilufar_enaga",
        "bio": "Bolajonlarni juda yaxshi ko'raman, o'zim ham 2 farzandning onasiman. 1 yoshdan 6 yoshgacha bolalarga mehrli parvarish, vaqtida ovqatlantirish, toza havoda sayr qildirish va tarbiyaviy o'yinlar o'ynatish. Sabrli va xushmuomalaliman.",
        "reviews": [
            {
                "author_name": "Madina Karimova",
                "author_user_id": 201,
                "rating": 5,
                "comment": "Nilufar opa bizning 2 yoshli qizimizga 1 yil mehr bilan qaradilar. O'z nabirasidek parvarish qiladilar, juda xotirjam ishga borib keldik. 100% tavsiya qilaman!"
            },
            {
                "author_name": "Sherzod aka",
                "author_user_id": 202,
                "rating": 5,
                "comment": "Farzandimiz juda tez o'rganib qoldi. O'z vaqtida uxlatish, ovqat berish qoidalariga qat'iy amal qiladilar. Rahmat katta!"
            }
        ]
    },
    {
        "user_id": 88803,
        "full_name": "Zuhra opa Ahmedova",
        "profession": "Farrosh",
        "age": 42,
        "district": "Mirzo Ulug'bek tumani",
        "work_type": "Soatbay",
        "expected_salary": "60 000 so'm / soatiga",
        "experience_years": "6 yil tajriba",
        "phone": "+998 97 889 44 21",
        "telegram": "@zuhra_tozalik",
        "bio": "Haftaning istalgan kunida soatbay yoki kunlik tozalikka boraman. Dazmollash, kiyim-kechaklarni tartiblash, changlarni artish va hammom-hojatxona dizenfeksiyasi.",
        "reviews": [
            {
                "author_name": "Nargiza opa",
                "author_user_id": 301,
                "rating": 5,
                "comment": "Zuhra opaga haftada 2 marta dazmol va uyni yig'ishtirishga murojaat qilamiz. Ishini bilib, tez va sifatli qiladilar."
            },
            {
                "author_name": "Rustam",
                "author_user_id": 302,
                "rating": 4,
                "comment": "Yaxshi tozaladilar, belgilangan vaqtda kelganlari uchun alohida rahmat."
            }
        ]
    },
    {
        "user_id": 88804,
        "full_name": "Zulayho Rahimova",
        "profession": "Farrosh",
        "age": 29,
        "district": "Yakkasaroy tumani",
        "work_type": "Kunlik (Bir martalik)",
        "expected_salary": "300 000 so'm / kuniga",
        "experience_years": "3 yil tajriba",
        "phone": "+998 94 654 33 22",
        "telegram": "@zulayho_clean",
        "bio": "Yosh, chaqqon va juda toza ishlayman. Oshxona shkaflarini ich-ichigacha tozalab, muzlatgich va pechkalarni yaltiratib beraman. Uy egalarining buyumlariga juda ehtiyotkorman.",
        "reviews": [
            {
                "author_name": "Dilshoda",
                "author_user_id": 401,
                "rating": 5,
                "comment": "Juda hushfe'l va chaqqon qiz ekan. Bir zumda butun uyni sarishta qildi. Rahmat, baraka topsin!"
            }
        ]
    },
    {
        "user_id": 88805,
        "full_name": "Gulnoza opa Umarova",
        "profession": "Enaga",
        "age": 49,
        "district": "Mirobod tumani",
        "work_type": "Yotib ishlash (Sutkalik)",
        "expected_salary": "6 000 000 so'm / oyiga",
        "experience_years": "12 yil tajriba",
        "phone": "+998 91 777 98 65",
        "telegram": "@gulnoza_enaga",
        "bio": "Katta tajribaga ega enagaman. Chaqaloqlikdan tortib maktab yoshigacha bolalarni parvarishlaganman. Bolaga sog'lom ovqatlar tayyorlash, massaj, rejimga o'rgatish. Yotib ishlashga roziman.",
        "reviews": [
            {
                "author_name": "Kamolaxon",
                "author_user_id": 501,
                "rating": 5,
                "comment": "Gulnoza opa oilamiz a'zosidek bo'lib qolganlar. Bolamizga ko'rsatgan mehri va g'amxo'rligi uchun minnatdormiz. Oltin qo'lli ayol!"
            },
            {
                "author_name": "Otabek",
                "author_user_id": 502,
                "rating": 5,
                "comment": "Chaqalog'imiz tunda bezovta bo'lganda ham juda sabr bilan qaraganlar. Juda katta tajribalari bor."
            }
        ]
    },
    {
        "user_id": 88806,
        "full_name": "Shahnoza Yusupova",
        "profession": "Enaga",
        "age": 33,
        "district": "Sergeli tumani",
        "work_type": "Oylik (Doimiy)",
        "expected_salary": "4 000 000 so'm / oyiga",
        "experience_years": "4 yil tajriba",
        "phone": "+998 99 222 34 56",
        "telegram": "@shahnoza_nanny",
        "bio": "Pedagogika yo'nalishida o'qiganman, bolalar bilan psixologik til topishishni yaxshi bilaman. Raqamlar, harflar, she'rlar yodlatish, rasm chizish. Mas'uliyatli va toza yuruvchi insonman.",
        "reviews": [
            {
                "author_name": "Dildora Nazarova",
                "author_user_id": 601,
                "rating": 5,
                "comment": "Shahnoza opa bolamizni maktabga tayyorlashda ham yordam berdilar. O'yinlar bilan harflarni o'rgatdi. Juda hursandmiz."
            }
        ]
    },
    {
        "user_id": 88807,
        "full_name": "Matluba opa Nazarova",
        "profession": "Farrosh",
        "age": 47,
        "district": "Shayxontohur tumani",
        "work_type": "Kunlik (Bir martalik)",
        "expected_salary": "350 000 so'm / kuniga",
        "experience_years": "9 yil tajriba",
        "phone": "+998 90 911 88 44",
        "telegram": "@matluba_tozalik",
        "bio": "Hovli va ko'p xonali uylarni chuqur tozalash (generalnaya uborka). Gilamlarni yuvish, parda ilish, barcha turdagi uy ishlarini bajaraman. Ishonchli, og'ir-bosiq ayolman.",
        "reviews": [
            {
                "author_name": "Farxod aka",
                "author_user_id": 701,
                "rating": 5,
                "comment": "Katta hovlimizni bir kunda sarishta qilib berdilar. Hamma joy porlab turibdi. Gap yo'q, qo'llari dard ko'rmasin!"
            }
        ]
    },
    {
        "user_id": 88808,
        "full_name": "Muyassar opa Jo'rayeva",
        "profession": "Enaga",
        "age": 51,
        "district": "Olmazor tumani",
        "work_type": "Kunlik (Bir martalik)",
        "expected_salary": "200 000 so'm / kuniga",
        "experience_years": "14 yil tajriba",
        "phone": "+998 95 123 77 88",
        "telegram": "@muyassar_opa",
        "bio": "Ota-onalar ish bilan yoki to'y-marosimga ketganda bolalarga qarab turish. Mehrli, shirinso'z, milliy urf-odatlarimizni biladigan, tajribali ona va buviman.",
        "reviews": [
            {
                "author_name": "Sevara",
                "author_user_id": 801,
                "rating": 5,
                "comment": "To'yimiz kuni 2 nafar bolamizga qarab berdilar. Bolalar juda xursand bo'lib o'ynashdi. Ishonchli va mehribon ayol."
            }
        ]
    }
]

SAMPLE_VACANCIES = [
    {
        "user_id": 99901,
        "title": "Chilonzorda 3 xonali uyga tozalik uchun chaqqon farrosh kerak",
        "profession": "Farrosh",
        "district": "Chilonzor tumani",
        "work_type": "Kunlik (Bir martalik)",
        "salary": "350 000 so'm / kuniga",
        "phone": "+998 90 111 22 33",
        "telegram": "@chilonzor_xonadon",
        "description": "3 xonali xonadonda to'liq tozalik qilish kerak: derazalar, oshxona mebellari va changlarni artish. Tozalash vositalari o'zimizdan beriladi."
    },
    {
        "user_id": 99902,
        "title": "2 yoshli qizaloqqa mehribon, doimiy enaga kerak",
        "profession": "Enaga",
        "district": "Yunusobod tumani",
        "work_type": "Oylik (Doimiy)",
        "salary": "4 500 000 so'm / oyiga",
        "phone": "+998 93 444 55 66",
        "telegram": "@yunusobod_oila",
        "description": "Dushanbadan jumagacha soat 09:00 dan 18:00 gacha. Bolani parvarishlash, ovqatlantirish va sayr qildirish. Uyda onasi ham bo'ladi."
    },
    {
        "user_id": 99903,
        "title": "Hovli xonadonga haftada 2 kun keladigan tozalik xodimi",
        "profession": "Farrosh",
        "district": "Mirzo Ulug'bek tumani",
        "work_type": "Kunlik (Bir martalik)",
        "salary": "400 000 so'm / har bir kelishiga",
        "phone": "+998 97 777 88 99",
        "telegram": "@mirzo_ulugbek_uy",
        "description": "Hovli uyni yig'ishtirish, dazmollash va sarishtalash. Halol, toza va tartibli ayol kerak."
    },
    {
        "user_id": 99904,
        "title": "Kechki payt (18:00 - 21:00) bolaga qarab turish uchun enaga",
        "profession": "Enaga",
        "district": "Yakkasaroy tumani",
        "work_type": "Soatbay",
        "salary": "50 000 so'm / soatiga",
        "phone": "+998 99 888 12 34",
        "telegram": "@yakkasaroy_nanny",
        "description": "Ona ishdan kelguncha 3 yoshli o'g'il bolaga qarab turish, qiziqarli o'yinlar o'ynatish."
    },
    {
        "user_id": 99905,
        "title": "Yangi ta'mirdan chiqqan kottejni tozalash",
        "profession": "Farrosh",
        "district": "Mirobod tumani",
        "work_type": "Kunlik (Bir martalik)",
        "salary": "500 000 so'm / kuniga",
        "phone": "+998 94 333 22 11",
        "telegram": "@mirobod_clean",
        "description": "Ta'mirdan so'ng pol va oynalarni tozalash. Barcha qulayliklar mavjud, tushlik ta'minlanadi."
    }
]

async def seed():
    await db.init_db()
    
    async with db.get_db() as conn:
        # Eski test ma'lumotlarini tozalaymiz
        await conn.execute("DELETE FROM reviews")
        await conn.execute("DELETE FROM vacancies")
        await conn.execute("DELETE FROM resumes")
        await conn.commit()

    print("🧹 Eski ma'lumotlar tozalandi...")

    # Mijoz buyurtmalarini kiritamiz
    for vac in SAMPLE_VACANCIES:
        await db.add_vacancy(
            user_id=vac["user_id"],
            title=vac["title"],
            profession=vac["profession"],
            district=vac["district"],
            work_type=vac["work_type"],
            salary=vac["salary"],
            phone=vac["phone"],
            telegram=vac["telegram"],
            description=vac["description"]
        )
    print(f"✅ {len(SAMPLE_VACANCIES)} ta mijoz buyurtmasi kiritildi.")

    # Farrosh va Enagalarni kiritamiz
    for w in SAMPLE_WORKERS:
        worker_id = await db.add_resume(
            user_id=w["user_id"],
            full_name=w["full_name"],
            profession=w["profession"],
            age=w["age"],
            district=w["district"],
            work_type=w["work_type"],
            expected_salary=w["expected_salary"],
            experience_years=w["experience_years"],
            phone=w["phone"],
            telegram=w["telegram"],
            bio=w["bio"]
        )

        # Har bir nomzod uchun izoh va baholarni kiritamiz
        for rev in w.get("reviews", []):
            await db.add_review(
                worker_id=worker_id,
                author_name=rev["author_name"],
                author_user_id=rev["author_user_id"],
                rating=rev["rating"],
                comment=rev["comment"]
            )

    print(f"✅ {len(SAMPLE_WORKERS)} ta Enaga va Farrosh anketasi izohlar va yulduzchalari bilan kiritildi!")

if __name__ == "__main__":
    asyncio.run(seed())
