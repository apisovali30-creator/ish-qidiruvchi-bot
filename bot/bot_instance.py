import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

logger = logging.getLogger(__name__)

bot: Bot | None = None
dp: Dispatcher = Dispatcher()

def get_bot() -> Bot:
    global bot
    if bot is None:
        if not BOT_TOKEN:
            logger.warning("BOT_TOKEN ko'rsatilmagan! Bot funksiyalari ishlamasligi mumkin.")
        bot = Bot(
            token=BOT_TOKEN or "1234567890:dummy_token_for_init",
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    return bot

async def notify_user(user_id: int, message_text: str) -> bool:
    """Foydalanuvchiga bot nomidan xabarnoma yuborish."""
    try:
        current_bot = get_bot()
        await current_bot.send_message(chat_id=user_id, text=message_text)
        return True
    except Exception as e:
        logger.error(f"Foydalanuvchiga xabar yuborishda xatolik ({user_id}): {e}")
        return False
