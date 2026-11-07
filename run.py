import asyncio
import logging
import uvicorn
from config import SERVER_HOST, SERVER_PORT, BOT_TOKEN, get_webapp_url
from server.app import app
from bot.bot_instance import get_bot, dp
from bot.handlers.start import router as start_router
from aiogram.types import MenuButtonWebApp, WebAppInfo

# Log tizimi
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("MAIN")

async def run_fastapi(server: uvicorn.Server):
    logger.info(f"🌐 FastAPI veb-server ishga tushmoqda: http://{SERVER_HOST}:{SERVER_PORT}")
    await server.serve()

async def run_bot():
    # Token tekshiruvi
    if not BOT_TOKEN or "dummy_token" in BOT_TOKEN or "1234567890:" in BOT_TOKEN:
        logger.warning(
            "\n" + "="*70 + "\n"
            "⚠️  DIQQAT: .env faylida haqiqiy BOT_TOKEN hali kiritilmagan!\n"
            "    Telegram Bot polling vaqtincha ishga tushmaydi, lekin\n"
            f"    FastAPI Mini App veb-serveri http://localhost:{SERVER_PORT} manzilida ISHLAMOQDA.\n"
            "    Haqiqiy Telegram botni ulash uchun .env fayliga BOT_TOKEN yozing.\n"
            + "="*70 + "\n"
        )
        return

    try:
        bot = get_bot()
        dp.include_router(start_router)

        # Telegram botning pastki chap burchagidagi [Open] MenuButton tugmasini o'rnatish
        url = get_webapp_url()
        if url.startswith("https://"):
            try:
                await bot.set_chat_menu_button(
                    menu_button=MenuButtonWebApp(
                        text="Open",
                        web_app=WebAppInfo(url=url)
                    )
                )
                logger.info(f"✅ Telegram Menu Button ('Open') muvaffaqiyatli o'rnatildi: {url}")
            except Exception as mb_err:
                logger.warning(f"Menu Button o'rnatishda xatolik: {mb_err}")

        logger.info("🤖 Telegram Bot (aiogram 3) polling ishga tushmoqda...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Telegram botni ishga tushirishda xatolik: {e}")

async def main():
    config = uvicorn.Config(
        app=app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info",
        loop="asyncio"
    )
    server = uvicorn.Server(config)

    # Ikkala vazifani parallel boshlash
    await asyncio.gather(
        run_fastapi(server),
        run_bot()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Loyiha to'xtatildi.")
