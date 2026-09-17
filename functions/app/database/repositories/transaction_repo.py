from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Transaction:
        tx = Transaction(**kwargs)
        self.session.add(tx)
        await self.session.flush()
        return tx

    async def get_by_order_id(self, order_id: int) -> Transaction | None:
        result = await self.session.execute(select(Transaction).where(Transaction.order_id == order_id))
        return result.scalar_one_or_none()

    async def update_status(self, order_id: int, status: str, tx_hash: str | None = None) -> Transaction | None:
        tx = await self.get_by_order_id(order_id)
        if tx:
            tx.status = status
            if tx_hash:
                tx.tx_hash = tx_hash
            if status == "confirmed":
                from datetime import datetime, timezone
                tx.confirmed_at = datetime.now(timezone.utc)
            await self.session.flush()
        return tx
