from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.order_repo import OrderRepository
from app.database.models.order import Order, OrderStatus
from app.services.rate_service import RateService


class ExchangeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.rate_service = RateService(session)

    async def create_order_from_quote(self, user_id: int, quote) -> Order:
        order_number = await self.order_repo.generate_next_order_number()
        return await self.order_repo.create(
            order_number=order_number,
            user_id=user_id,
            input_currency="IQD",
            input_amount=quote.input_amount,
            output_currency=quote.currency,
            output_amount=quote.output_amount,
            network=quote.network,
            exchange_rate=quote.rate,
            fee=quote.fee,
            quote_id=quote.quote_id,
            status=OrderStatus.WAITING_PAYMENT.value,
        )

    async def get_order(self, order_id: int):
        return await self.order_repo.get_by_id(order_id)

    async def get_user_orders(self, user_id: int, limit: int = 20):
        return await self.order_repo.get_user_orders(user_id, limit)

    async def update_status(self, order_id: int, status: OrderStatus):
        return await self.order_repo.update_status(order_id, status)

    async def set_wallet_address(self, order_id: int, wallet_address: str):
        return await self.order_repo.update_wallet_address(order_id, wallet_address)

    async def get_pending_orders(self):
        return await self.order_repo.get_pending_orders()

    async def get_all_orders(self, limit: int = 50):
        return await self.order_repo.get_all_orders(limit)

    async def count_by_status(self):
        return await self.order_repo.count_by_status()

    async def total_volume(self):
        return await self.order_repo.total_volume()
