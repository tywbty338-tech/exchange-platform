from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.order import Order, OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Order:
        order = Order(**kwargs)
        self.session.add(order)
        await self.session.flush()
        return order

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def get_by_order_number(self, order_number: str) -> Order | None:
        result = await self.session.execute(select(Order).where(Order.order_number == order_number))
        return result.scalar_one_or_none()

    async def get_user_orders(self, user_id: int, limit: int = 20) -> list[Order]:
        result = await self.session.execute(
            select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def get_pending_orders(self) -> list[Order]:
        pending = [OrderStatus.WAITING_PAYMENT.value, OrderStatus.PAYMENT_PROCESSING.value,
                   OrderStatus.PAYMENT_CONFIRMED.value, OrderStatus.WAITING_WALLET.value]
        result = await self.session.execute(
            select(Order).where(Order.status.in_(pending)).order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_orders(self, limit: int = 50) -> list[Order]:
        result = await self.session.execute(select(Order).order_by(Order.created_at.desc()).limit(limit))
        return list(result.scalars().all())

    async def update_status(self, order_id: int, status: OrderStatus) -> Order | None:
        order = await self.get_by_id(order_id)
        if order:
            order.status = status.value
            if status == OrderStatus.COMPLETED:
                from datetime import datetime, timezone
                order.completed_at = datetime.now(timezone.utc)
            await self.session.flush()
        return order

    async def update_wallet_address(self, order_id: int, wallet_address: str) -> Order | None:
        order = await self.get_by_id(order_id)
        if order:
            order.wallet_address = wallet_address
            await self.session.flush()
        return order

    async def generate_next_order_number(self) -> str:
        result = await self.session.execute(select(func.max(Order.id)))
        max_id = result.scalar()
        return f"#{(max_id or 0) + 1:04d}"

    async def count_by_status(self) -> dict[str, int]:
        result = await self.session.execute(select(Order.status, func.count(Order.id)).group_by(Order.status))
        return {row[0]: row[1] for row in result.all()}

    async def total_volume(self) -> float:
        result = await self.session.execute(select(func.sum(Order.input_amount)))
        return result.scalar() or 0
