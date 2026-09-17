from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.config import get_settings
from app.schemas import AdminRateUpdate, StatsResponse
from app.services.rate_service import RateService
from app.services.exchange_service import ExchangeService
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.quote_repo import QuoteRepository
from app.api.routes.auth import get_current_user

router = APIRouter()
settings = get_settings()


def require_admin(user):
    if user.telegram_id not in settings.admin_id_set:
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/stats", response_model=StatsResponse)
async def admin_stats(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    require_admin(user)
    user_repo = UserRepository(session)
    exchange_service = ExchangeService(session)
    status_counts = await exchange_service.count_by_status()
    return StatsResponse(
        total_users=await user_repo.count_users(),
        total_orders=sum(status_counts.values()),
        pending_orders=sum(status_counts.get(s, 0) for s in ["WAITING_PAYMENT", "PAYMENT_PROCESSING", "WAITING_WALLET"]),
        completed_orders=status_counts.get("COMPLETED", 0),
        total_volume=await exchange_service.total_volume(),
    )


@router.get("/rates")
async def admin_rates(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    require_admin(user)
    rate_service = RateService(session)
    rates = await rate_service.get_all_rates()
    return [{"currency": r.currency, "network": r.network, "rate": r.rate, "fee_type": r.fee_type,
             "fee_value": r.fee_value, "min_amount": r.min_amount, "max_amount": r.max_amount,
             "active": r.active} for r in rates]


@router.put("/rates/{currency}/{network}")
async def admin_update_rate(
    currency: str,
    network: str,
    req: AdminRateUpdate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    require_admin(user)
    rate_service = RateService(session)
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    rate = await rate_service.update_rate(currency, network, **updates)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    return {"success": True, "rate": {"currency": rate.currency, "network": rate.network, "rate": rate.rate}}
