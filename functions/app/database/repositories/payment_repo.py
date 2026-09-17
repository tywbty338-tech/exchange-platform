from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.payment import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Payment:
        payment = Payment(**kwargs)
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def get_by_order_id(self, order_id: int) -> Payment | None:
        result = await self.session.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalar_one_or_none()

    async def update_status(self, order_id: int, status: str, provider_reference: str | None = None) -> Payment | None:
        payment = await self.get_by_order_id(order_id)
        if payment:
            payment.status = status
            if provider_reference:
                payment.provider_reference = provider_reference
            await self.session.flush()
        return payment
