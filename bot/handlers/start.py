import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    MenuButtonWebApp
)
from config import get_webapp_url, ADMIN_IDS
import database.db as db

logger = logging.getLogger(__name__)
router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def get_start_inline_keyboard(user_id: int = 0) -> InlineKeyboardMarkup:
    url = get_webapp_url()
    admin_url = f"{url}/admin" if url.startswith("http") else url
    
    buttons = [
        [
            InlineKeyboardButton(
                text="🚀 Ilovani ochish (Mini App)",
                web_app=WebAppInfo(url=url) if url.startswith("https://") else None,
                url=url if not url.startswith("https://") else None
            )
        ]
    ]

    # Admin bo'lsa, xavfsiz Admin Panel tugmasini ham qo'shamiz
    if is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(
                text="👑 Google Admin Panelni ochish",
                url=admin_url
            )
        ])

    buttons.extend([
        [
            InlineKeyboardButton(
                text="🧹 Farroshlar",
                web_app=WebAppInfo(url=f"{url}#farrosh") if url.startswith("https://") else None,
                url=f"{url}#farrosh" if not url.startswith("https://") else None
            ),
            InlineKeyboardButton(
                text="👶 Enagalar",
                web_app=WebAppInfo(url=f"{url}#enaga") if url.startswith("https://") else None,
                url=f"{url}#enaga" if not url.startswith("https://") else None
            )
        ],
        [
            InlineKeyboardButton(
                text="➕ Anketa / E'lon berish",
                web_app=WebAppInfo(url=f"{url}#create") if url.startswith("https://") else None,
                url=f"{url}#create" if not url.startswith("https://") else None
            )
        ]
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_start_reply_keyboard(user_id: int = 0) -> ReplyKeyboardMarkup:
    url = get_webapp_url()
    
    rows = [
        [
            KeyboardButton(
                text="📱 Platformani ochish",
                web_app=WebAppInfo(url=url) if url.startswith("https://") else None
            )
        ]
    ]

    if is_admin(user_id):
        rows.append([
            KeyboardButton(text="👑 Admin Panel"),
            KeyboardButton(text="📊 Statistika")
        ])

    rows.append([
        KeyboardButton(text="ℹ️ Bot va Ilova haqida")
    ])

    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    user_name = message.from_user.first_name if message.from_user else "do'stim"
    url = get_webapp_url()
    logger.info(f"[/start] qabul qilindi: ID={user_id}, Ism={user_name}")

    # Xabar yozish qatori yonidagi MenuButton ni avtomatik 'Open' (Ilova) ga sozlash
    if url.startswith("https://") and message.bot:
        try:
            await message.bot.set_chat_menu_button(
                chat_id=message.chat.id,
                menu_button=MenuButtonWebApp(
                    text="Open",
                    web_app=WebAppInfo(url=url)
                )
            )
        except Exception as e:
            logger.warning(f"Chat menu button sozlashda xatolik: {e}")

    # AGAR FOYDALANUVCHI ADMIN BO'LSA (masalan: 5150570662)
    if is_admin(user_id):
        admin_greeting = (
            f"👑 <b>Assalomu alaykum, Hurmatli Bosh Admin ({user_name})!</b> 👋\n\n"
            f"🆔 <b>Sizning ID raqamingiz:</b> <code>{user_id}</code>\n"
            f"🛡 <b>Huquq holati:</b> Boshqaruvchi Admin (Tasdiqlangan)\n\n"
            f"Siz bot va platformaning to'liq admin vakolatiga egasiz. "
            f"Foydalanuvchilar qoldirgan barcha yangi e'lonlar, anketalar va sharhlar "
            f"to'g'ridan-to'g'ri profilingizga xabarnoma sifatida keladi.\n\n"
            f"Platformani boshqarish uchun quyidagi tugmalardan foydalaning 👇"
        )
        try:
            await message.answer(
                text=admin_greeting,
                reply_markup=get_start_inline_keyboard(user_id)
            )
            await message.answer(
                "Boshqaruv menyusi 👇",
                reply_markup=get_start_reply_keyboard(user_id)
            )
        except Exception as e:
            logger.error(f"Admin start xabarida xatolik: {e}")
        return

    # ODDIY FOYDALANUVCHILAR UCHUN
    text = (
        f"Assalomu alaykum, <b>{user_name}</b>! 👋\n\n"
        f"🌟 <b>Ishonchli Farrosh va Enagalar Platformasiga xush kelibsiz!</b>\n\n"
        f"Ushbu platforma Toshkent shahri bo'ylab xonadonlar uchun sinalgan tozalik ustalari (farroshlar) "
        f"va mehribon enagalarni eng tez va qulay tarzda topish imkonini beradi.\n\n"
        f"Bu yerda oliy ma'lumot yoki diplom shart emas — eng asosiysi halollik, tajriba, "
        f"mijozlarning haqqoniy yulduzchalari (⭐) va izohlaridir!\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>Asosiy imkoniyatlar:</b>\n\n"
        f"🧹 <b>Farroshlar katalogi:</b>\n"
        f"• Uylarni boshdan-oyoq tozalash, deraza yuvish, kunlik yoki doimiy tozalik xodimlari;\n"
        f"• Tumanlar bo'yicha saralash, yoshi, tajribasi va narxlari bilan tanishish;\n"
        f"• Mijozlarning haqiqiy baholari va izohlarini o'qish.\n\n"
        f"👶 <b>Enagalar katalogi:</b>\n"
        f"• Kichkintoylarga mehr bilan qarovchi, tarbiyali va mas'uliyatli enagalar;\n"
        f"• Soatbay, kunlik yoki yotib ishlash shartlari bo'yicha tanlov.\n\n"
        f"⭐ <b>Haqqoniy baholash va izohlar:</b>\n"
        f"• Ish yakunlanganidan so'ng xodimga 1 dan 5 yulduzgacha baho va izoh qoldirish imkoniyati.\n\n"
        f"➕ <b>Ayollar uchun ish topish:</b>\n"
        f"• O'z anketangizni (yosh, tuman, narx, telefon) 1 daqiqada kiritib, darhol buyurtmalar oling!\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"👇 <b>Ilovani ishga tushirish uchun:</b>\n"
        f"Quyidagi <b>'🚀 Ilovani ochish'</b> tugmasini bosing yoki chat burchagidagi <b>'Open'</b> tugmasidan foydalaning!"
    )

    try:
        await message.answer(
            text=text,
            reply_markup=get_start_inline_keyboard(user_id)
        )
        await message.answer(
            "Xabar yozish qatori yonidagi <b>'Open'</b> tugmasi yoki quyidagi doimiy menyu orqali ham ilovani ochishingiz mumkin 👇",
            reply_markup=get_start_reply_keyboard(user_id)
        )
    except Exception as e:
        logger.error(f"Xabar yuborishda xatolik: {e}")
        await message.answer(text=text)

@router.message(Command("admin"))
@router.message(F.text == "👑 Admin Panel")
@router.message(F.text == "📊 Statistika")
async def handle_admin_command(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    if not is_admin(user_id):
        await message.answer("⛔️ Kechirasiz, sizda admin huquqlari mavjud emas.")
        return

    url = get_webapp_url()
    admin_url = f"{url}/admin" if url.startswith("http") else url

    try:
        stats = await db.get_admin_stats()
        farrosh_count = stats.get("farrosh_count", 0)
        enaga_count = stats.get("enaga_count", 0)
        vacancies_count = stats.get("total_vacancies", 0)
        avg_rating = stats.get("avg_rating", 5.0)
        reviews_count = stats.get("total_reviews", 0)
    except Exception as e:
        logger.error(f"Stats olishda xatolik: {e}")
        farrosh_count = enaga_count = vacancies_count = reviews_count = 0
        avg_rating = 5.0

    stats_text = (
        "👑 <b>Hurmatli Admin! Oqila Boshqaruv Markazi</b>\n"
        f"🆔 Sizning profilingiz: <code>{user_id}</code> (Bosh Admin)\n\n"
        "📊 <b>Platformaning real-vaqt statistikasi:</b>\n"
        f"• 🧹 <b>Farroshlar:</b> {farrosh_count} nafar\n"
        f"• 👶 <b>Enagalar:</b> {enaga_count} nafar\n"
        f"• 📋 <b>Buyurtmalar:</b> {vacancies_count} ta\n"
        f"• ⭐ <b>Mijozlar reytingi:</b> {avg_rating:.1f} ({reviews_count} ta izoh)\n\n"
        "🌐 <b>Google Admin Panel:</b>\n"
        f"Barcha nomzodlarni boshqarish, o'chirish va sharhlarni nazorat qilish uchun "
        f"Google Chrome brauzeridan quyidagi havola orqali kiring:\n"
        f"👉 <a href=\"{admin_url}\">{admin_url}</a>\n"
        f"(Faqat sizning Google pochtangiz: <b>aliapisov11@gmail.com</b>)"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👑 Google Admin Panelni ochish",
                    url=admin_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚀 Mini App'ni ochish",
                    web_app=WebAppInfo(url=url) if url.startswith("https://") else None,
                    url=url if not url.startswith("https://") else None
                )
            ]
        ]
    )

    await message.answer(stats_text, reply_markup=kb)

@router.message(F.text == "ℹ️ Bot va Ilova haqida")
@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    help_text = (
        "ℹ️ <b>Loyiha haqida batafsil:</b>\n\n"
        "💡 <b>Loyiha maqsadi:</b> Diplomsiz ayollarga munosib va halol ish topishda ko'maklashish hamda xonadonlar uchun eng ishonchli, yaxshi izoh olgan farrosh va enagalarni tavsiya qilish.\n\n"
        "📱 <b>Mini App bo'limlari:</b>\n"
        "1. <b>'🧹 Farroshlar'</b> — Tajribali tozalik ustalari ro'yxati.\n"
        "2. <b>'👶 Enagalar'</b> — Mehribon va ishonchli bolalar parvarishlovchilari.\n"
        "3. <b>'📋 Buyurtmalar'</b> — Xonadon egalarining ish takliflari.\n"
        "4. <b>'⭐ Izoh qoldirish'</b> — Ishni bitirgach, xodim profiliga o'tib, yulduzchalar va samimiy fikr bildirish.\n"
        "5. <b>'➕ Anketa berish'</b> — O'zingiz haqingizda e'lon berish."
    )
    user_id = message.from_user.id if message.from_user else 0
    try:
        await message.answer(
            text=help_text,
            reply_markup=get_start_inline_keyboard(user_id)
        )
    except Exception as e:
        logger.error(f"Yordam yuborishda xatolik: {e}")
        await message.answer(text=help_text)

# Har qanday boshqa matnli xabar kelganda ham yo'naltirish
@router.message(F.text)
async def handle_other_messages(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    logger.info(f"[Text message] qabul qilindi: '{message.text}' from {user_id}")
    await message.answer(
        "Iltimos, platformadan foydalanish uchun quyidagi tugmani bosing yoki /start yuboring:",
        reply_markup=get_start_inline_keyboard(user_id)
    )
