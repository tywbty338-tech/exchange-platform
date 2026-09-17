import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.quote import Quote


class QuoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, currency: str, network: str,
                     input_amount: float, rate: float, fee: float, output_amount: float,
                     validity_seconds: int = 60) -> Quote:
        quote = Quote(
            quote_id=str(uuid.uuid4()),
            user_id=user_id,
            currency=currency,
            network=network,
            input_amount=input_amount,
            rate=rate,
            fee=fee,
            output_amount=output_amount,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=validity_seconds),
        )
        self.session.add(quote)
        await self.session.flush()
        return quote

    async def get_by_quote_id(self, quote_id: str) -> Quote | None:
        result = await self.session.execute(select(Quote).where(Quote.quote_id == quote_id))
        return result.scalar_one_or_none()

    async def mark_used(self, quote_id: str) -> Quote | None:
        quote = await self.get_by_quote_id(quote_id)
        if quote:
            quote.used = True
            await self.session.flush()
        return quote
