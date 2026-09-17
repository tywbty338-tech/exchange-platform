from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.quote_repo import QuoteRepository
from app.database.repositories.rate_repo import RateRepository


class QuoteService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.quote_repo = QuoteRepository(session)
        self.rate_repo = RateRepository(session)

    async def create_quote(self, user_id: int, currency: str, network: str,
                           input_amount: float, validity_seconds: int = 60):
        rate_obj = await self.rate_repo.get_active_rate(currency, network)
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

        output_amount = (input_amount - fee) * rate_obj.rate

        quote = await self.quote_repo.create(
            user_id=user_id,
            currency=currency,
            network=network,
            input_amount=input_amount,
            rate=rate_obj.rate,
            fee=fee,
            output_amount=output_amount,
            validity_seconds=validity_seconds,
        )
        return quote

    async def get_quote(self, quote_id: str):
        return await self.quote_repo.get_by_quote_id(quote_id)

    async def use_quote(self, quote_id: str):
        return await self.quote_repo.mark_used(quote_id)
