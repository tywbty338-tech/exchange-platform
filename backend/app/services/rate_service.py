from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.rate_repo import RateRepository
from app.database.models.rate import Rate


class RateService:
    def __init__(self, session: AsyncSession):
        self.repo = RateRepository(session)

    async def get_rate(self, currency: str, network: str) -> Rate | None:
        return await self.repo.get_active_rate(currency, network)

    async def calculate_output(self, currency: str, network: str, input_amount: float) -> tuple[float, float, float]:
        rate_obj = await self.get_rate(currency, network)
        if not rate_obj:
            raise ValueError(f"No active rate for {currency}/{network}")
        if input_amount < rate_obj.min_amount:
            raise ValueError(f"Minimum amount is {rate_obj.min_amount}")
        if input_amount > rate_obj.max_amount:
            raise ValueError(f"Maximum amount is {rate_obj.max_amount}")

        if rate_obj.fee_type == "fixed":
            fee = rate_obj.fee_value
        elif rate_obj.fee_type == "percent":
            fee = input_amount * (rate_obj.fee_value / 100)
        else:
            fee = 0

        net_amount = input_amount - fee
        output_amount = net_amount * rate_obj.rate
        return output_amount, fee, rate_obj.rate

    async def init_default_rates(self) -> None:
        await self.repo.get_or_create_rate("USDT", "TRC20", 0.000704, "percent", 2, 3000, 5000000)
        await self.repo.get_or_create_rate("USDT", "TON", 0.000704, "percent", 2, 3000, 5000000)
        await self.repo.get_or_create_rate("TON", "TON", 0.000112, "percent", 2, 3000, 5000000)

    async def update_rate(self, currency: str, network: str, **kwargs) -> Rate | None:
        return await self.repo.update_rate(currency, network, **kwargs)

    async def get_all_rates(self) -> list[Rate]:
        return await self.repo.get_all_rates()
