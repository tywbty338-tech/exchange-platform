from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.wallet import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, currency: str, network: str, address: str, label: str | None = None) -> Wallet:
        wallet = Wallet(user_id=user_id, currency=currency, network=network, address=address, label=label)
        self.session.add(wallet)
        await self.session.flush()
        return wallet

    async def get_user_wallets(self, user_id: int) -> list[Wallet]:
        result = await self.session.execute(select(Wallet).where(Wallet.user_id == user_id))
        return list(result.scalars().all())

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        result = await self.session.execute(select(Wallet).where(Wallet.id == wallet_id))
        return result.scalar_one_or_none()

    async def delete(self, wallet_id: int) -> bool:
        wallet = await self.get_by_id(wallet_id)
        if wallet:
            await self.session.delete(wallet)
            await self.session.flush()
            return True
        return False
