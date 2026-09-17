from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from app.core.config import get_settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    settings = get_settings()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": settings.webapp_url or "https://example.com"})],
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


@router.callback_query(F.data == "rates")
async def cb_rates(callback: CallbackQuery):
    from app.core.database import async_session_factory
    from app.services.rate_service import RateService

    async with async_session_factory() as session:
        rate_service = RateService(session)
        rates = await rate_service.get_all_rates()

    text = "💱 <b>أسعار الصرف</b>\n\n"
    for r in rates:
        icon = "💵" if r.currency == "USDT" else "💎"
        rate_iqd = int(1 / r.rate) if r.rate else 0
        text += f"{icon} <b>{r.currency}</b>\n1 {r.currency} = {rate_iqd:,} د.ع\n\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": get_settings().webapp_url or "https://example.com"})],
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "my_orders")
async def cb_my_orders(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 فتح التطبيق", web_app={"url": get_settings().webapp_url or "https://example.com"})],
    ])
    await callback.message.edit_text("📋 افتح التطبيق لعرض طلباتك", reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "support")
async def cb_support(callback: CallbackQuery):
    await callback.message.edit_text("🎧 للدعم الفني: @support", parse_mode="HTML")
    await callback.answer()


def setup_handlers(dp):
    dp.include_router(router)
