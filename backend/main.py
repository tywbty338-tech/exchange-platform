import asyncio
import logging
import sys

from app.core.config import get_settings
from app.core.database import init_db, async_session_factory
from app.services.rate_service import RateService
from app.api.app import app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


async def on_startup():
    settings = get_settings()
    logger.info("Starting exchange platform...")
    logger.info(f"TEST_MODE: {settings.test_mode}")
    await init_db()
    logger.info("Database initialized")

    async with async_session_factory() as session:
        rate_service = RateService(session)
        await rate_service.init_default_rates()
        await session.commit()
    logger.info("Default rates initialized")


async def run_bot():
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from app.bot.handlers import setup_handlers

    settings = get_settings()
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    setup_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started in polling mode")
    await dp.start_polling(bot)


async def run_api():
    import uvicorn
    settings = get_settings()
    config = uvicorn.Config(app, host=settings.api_host, port=settings.api_port)
    server = uvicorn.Server(config)
    logger.info(f"API running on {settings.api_host}:{settings.api_port}")
    await server.serve()


async def main():
    await on_startup()

    settings = get_settings()
    if settings.webapp_url:
        await asyncio.gather(run_bot(), run_api())
    else:
        await asyncio.gather(run_bot(), run_api())


if __name__ == "__main__":
    asyncio.run(main())
