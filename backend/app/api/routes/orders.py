from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import OrderCreate, OrderResponse, WalletAddressUpdate
from app.services.exchange_service import ExchangeService
from app.services.quote_service import QuoteService
from app.services.wallet_service import WalletService
from app.services.payment_service import PaymentService
from app.database.models.order import OrderStatus
from app.core.config import get_settings
from app.api.routes.auth import get_current_user

router = APIRouter()
settings = get_settings()


@router.post("/orders", response_model=OrderResponse)
async def create_order(
    req: OrderCreate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    quote_service = QuoteService(session)
    quote = await quote_service.get_quote(req.quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    if quote.is_expired:
        raise HTTPException(status_code=410, detail="Quote expired")

    exchange_service = ExchangeService(session)
    order = await exchange_service.create_order_from_quote(user.id, quote)
    await quote_service.use_quote(req.quote_id)

    payment_service = PaymentService(session, settings.payment_provider)
    await payment_service.create_payment(order.id, order.input_amount)

    return OrderResponse.model_validate(order)


@router.get("/orders", response_model=list[OrderResponse])
async def list_orders(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    limit: int = 20,
):
    exchange_service = ExchangeService(session)
    orders = await exchange_service.get_user_orders(user.id, limit)
    return [OrderResponse.model_validate(o) for o in orders]


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    exchange_service = ExchangeService(session)
    order = await exchange_service.get_order(order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)


@router.post("/orders/{order_id}/wallet")
async def set_wallet(
    order_id: int,
    req: WalletAddressUpdate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    exchange_service = ExchangeService(session)
    order = await exchange_service.get_order(order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    wallet_service = WalletService(session, settings.test_mode)
    if not wallet_service.is_valid_address(req.wallet_address, order.network):
        raise HTTPException(status_code=400, detail="Invalid wallet address")

    await exchange_service.set_wallet_address(order_id, req.wallet_address)
    return {"success": True}


@router.post("/orders/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    exchange_service = ExchangeService(session)
    order = await exchange_service.get_order(order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    if not order.wallet_address:
        raise HTTPException(status_code=400, detail="Wallet address required")

    wallet_service = WalletService(session, settings.test_mode)
    try:
        result = await wallet_service.send_tokens(
            order_id=order.id,
            currency=order.output_currency,
            network=order.network,
            amount=order.output_amount,
            destination=order.wallet_address,
        )
        await exchange_service.update_status(order.id, OrderStatus.COMPLETED)
        return {"success": True, "tx_hash": result.get("tx_hash")}
    except Exception as e:
        await exchange_service.update_status(order.id, OrderStatus.TRANSFER_FAILED)
        raise HTTPException(status_code=500, detail=str(e))
