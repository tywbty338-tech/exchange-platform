from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.rate import Rate


class RateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_rate(self, currency: str, network: str) -> Rate | None:
        result = await self.session.execute(
            select(Rate).where(Rate.currency == currency, Rate.network == network, Rate.active == True)
        )
        return result.scalar_one_or_none()

    async def get_or_create_rate(self, currency: str, network: str, rate: float = 1.0,
                                  fee_type: str = "fixed", fee_value: float = 0,
                                  min_amount: float = 0, max_amount: float = 999999999) -> Rate:
        existing = await self.get_active_rate(currency, network)
        if existing:
            existing.rate = rate
            existing.fee_type = fee_type
            existing.fee_value = fee_value
            existing.min_amount = min_amount
            existing.max_amount = max_amount
            await self.session.flush()
            return existing
        new_rate = Rate(currency=currency, network=network, rate=rate, fee_type=fee_type,
                        fee_value=fee_value, min_amount=min_amount, max_amount=max_amount, active=True)
        self.session.add(new_rate)
        await self.session.flush()
        return new_rate

    async def update_rate(self, currency: str, network: str, **kwargs) -> Rate | None:
        rate_obj = await self.get_active_rate(currency, network)
        if rate_obj:
            for k, v in kwargs.items():
                if hasattr(rate_obj, k):
                    setattr(rate_obj, k, v)
            await self.session.flush()
        return rate_obj

    async def get_all_rates(self) -> list[Rate]:
        result = await self.session.execute(select(Rate).where(Rate.active == True))
        return list(result.scalars().all())
