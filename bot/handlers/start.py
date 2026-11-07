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
from config import get_webapp_url

logger = logging.getLogger(__name__)
router = Router()

def get_start_inline_keyboard() -> InlineKeyboardMarkup:
    url = get_webapp_url()
    
    if url.startswith("https://"):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Ilovani ochish (Mini App)",
                        web_app=WebAppInfo(url=url)
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🧹 Farroshlar",
                        web_app=WebAppInfo(url=f"{url}#farrosh")
                    ),
                    InlineKeyboardButton(
                        text="👶 Enagalar",
                        web_app=WebAppInfo(url=f"{url}#enaga")
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="➕ Anketa / E'lon berish",
                        web_app=WebAppInfo(url=f"{url}#create")
                    )
                ]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🌐 Ilovani brauzerda ochish",
                        url=url
                    )
                ]
            ]
        )

def get_start_reply_keyboard() -> ReplyKeyboardMarkup:
    url = get_webapp_url()
    
    if url.startswith("https://"):
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="📱 Platformani ochish",
                        web_app=WebAppInfo(url=url)
                    )
                ],
                [
                    KeyboardButton(text="ℹ️ Bot va Ilova haqida")
                ]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ℹ️ Bot va Ilova haqida")
                ]
            ],
            resize_keyboard=True
        )

@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    user_name = message.from_user.first_name if message.from_user else "do'stim"
    url = get_webapp_url()
    logger.info(f"[/start] qabul qilindi: ID={message.from_user.id if message.from_user else 'Unknown'}, Ism={user_name}")

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
            reply_markup=get_start_inline_keyboard()
        )
        await message.answer(
            "Xabar yozish qatori yonidagi <b>'Open'</b> tugmasi yoki quyidagi doimiy menyu orqali ham ilovani ochishingiz mumkin 👇",
            reply_markup=get_start_reply_keyboard()
        )
    except Exception as e:
        logger.error(f"Xabar yuborishda xatolik: {e}")
        await message.answer(text=text)

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
    try:
        await message.answer(
            text=help_text,
            reply_markup=get_start_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Yordam yuborishda xatolik: {e}")
        await message.answer(text=help_text)

# Har qanday boshqa matnli xabar kelganda ham yo'naltirish
@router.message(F.text)
async def handle_other_messages(message: Message) -> None:
    logger.info(f"[Text message] qabul qilindi: '{message.text}' from {message.from_user.id if message.from_user else 'unknown'}")
    await message.answer(
        "Iltimos, platformadan foydalanish uchun quyidagi tugmani bosing yoki /start yuboring:",
        reply_markup=get_start_inline_keyboard()
    )
