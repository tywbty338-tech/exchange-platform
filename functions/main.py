"""
Firebase Cloud Functions — Exchange Bot + API
"""
import os
import sys
import logging
from pathlib import Path

functions_dir = Path(__file__).resolve().parent
if str(functions_dir) not in sys.path:
    sys.path.insert(0, str(functions_dir))

os.environ.setdefault("DATABASE_URL", f"sqlite+aiosqlite:///{functions_dir / 'exchange.db'}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

api = FastAPI(title="Exchange Platform")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = None
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    webapp_url = os.environ.get("WEBAPP_URL", "https://example.com")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": webapp_url})],
        [InlineKeyboardButton(text="💱 أسعار الصرف", callback_data="rates")],
        [InlineKeyboardButton(text="📋 طلباتي", callback_data="my_orders")],
        [InlineKeyboardButton(text="🎧 الدعم", callback_data="support")],
    ])
    text = (
        "💠 <b>EXCHANGE</b>\n"
        "Digital Exchange Platform\n\n"
        "حول رصيد آسياسيل إلى USDT أو TON\n"
        "بأسعار مباشرة وآمنة\n\n"
        "🟢 الخدمة متاحة الآن"
    )
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@dp.callback_query(F.data == "rates")
async def cb_rates(callback: CallbackQuery):
    webapp_url = os.environ.get("WEBAPP_URL", "https://example.com")
    try:
        from app.core.database import async_session_factory
        from app.services.rate_service import RateService
        async with async_session_factory() as session:
            rate_service = RateService(session)
            rates = await rate_service.get_all_rates()
    except Exception:
        rates = []

    text = "💱 <b>أسعار الصرف</b>\n\n"
    if rates:
        for r in rates:
            icon = "💵" if r.currency == "USDT" else "💎"
            rate_iqd = int(1 / r.rate) if r.rate else 0
            text += f"{icon} <b>{r.currency}</b>\n1 {r.currency} = {rate_iqd:,} د.ع\n\n"
    else:
        text += "جاري تحميل الأسعار..."

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": webapp_url})],
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "my_orders")
async def cb_my_orders(callback: CallbackQuery):
    webapp_url = os.environ.get("WEBAPP_URL", "https://example.com")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": webapp_url})],
    ])
    await callback.message.edit_text("📋 افتح التطبيق لعرض طلباتك", reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "support")
async def cb_support(callback: CallbackQuery):
    await callback.message.edit_text("🎧 للدعم الفني: @support", parse_mode="HTML")
    await callback.answer()


@api.post("/api/webhook")
async def telegram_webhook(request: Request):
    global bot
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@api.get("/api/health")
async def health():
    return {"status": "ok", "version": "2.0-firebase"}


@api.get("/api/rates")
async def get_rates():
    try:
        from app.core.database import async_session_factory
        from app.services.rate_service import RateService
        async with async_session_factory() as session:
            rate_service = RateService(session)
            rates = await rate_service.get_all_rates()
        return [{"currency": r.currency, "network": r.network, "rate": r.rate,
                 "fee_type": r.fee_type, "fee_value": r.fee_value,
                 "min_amount": r.min_amount, "max_amount": r.max_amount,
                 "active": r.active} for r in rates]
    except Exception as e:
        return {"error": str(e)}


@api.post("/api/orders")
async def create_order(request: Request):
    return {"status": "coming_soon", "message": "Order system coming soon"}


@api.get("/api/quotes")
async def get_quotes():
    return []


@api.get("/api/wallets")
async def get_wallets():
    return []


@api.post("/api/auth/login")
async def login(request: Request):
    return {"token": "mock-token", "user": {"id": 1}}


STATIC_DIR = functions_dir / "static"
if STATIC_DIR.exists():
    if (STATIC_DIR / "assets").exists():
        api.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    @api.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))


def init_bot():
    global bot
    token = os.environ.get("BOT_TOKEN", "")
    if token:
        bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
        logger.info("Bot initialized for webhook mode")
    else:
        logger.warning("BOT_TOKEN not set")


@api.on_event("startup")
async def startup():
    init_bot()
    try:
        from app.core.database import init_db
        await init_db()
        from app.core.database import async_session_factory
        from app.services.rate_service import RateService
        async with async_session_factory() as session:
            rate_service = RateService(session)
            await rate_service.init_default_rates()
            await session.commit()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"DB init error: {e}")


def main(request=None, context=None):
    return api
