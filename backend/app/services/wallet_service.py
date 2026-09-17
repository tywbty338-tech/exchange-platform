import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.transaction_repo import TransactionRepository

logger = logging.getLogger(__name__)


class WalletProvider:
    async def send(self, currency: str, network: str, amount: float, destination: str) -> dict:
        raise NotImplementedError


class MockWalletProvider(WalletProvider):
    async def send(self, currency: str, network: str, amount: float, destination: str) -> dict:
        tx_hash = f"0x{uuid.uuid4().hex[:16]}"
        logger.info(f"[MOCK] Sent {amount} {currency} ({network}) to {destination} | TX: {tx_hash}")
        return {"tx_hash": tx_hash, "status": "confirmed"}


class TONWalletProvider(WalletProvider):
    async def send(self, currency: str, network: str, amount: float, destination: str) -> dict:
        raise NotImplementedError("TON wallet provider not yet configured")


class WalletService:
    def __init__(self, session: AsyncSession, test_mode: bool = True):
        self.session = session
        self.tx_repo = TransactionRepository(session)
        self.provider = MockWalletProvider() if test_mode else TONWalletProvider()

    async def create_transaction(self, order_id: int, currency: str, network: str,
                                 amount: float, destination: str):
        return await self.tx_repo.create(order_id=order_id, currency=currency, network=network,
                                         amount=amount, destination_address=destination, status="pending")

    async def send_tokens(self, order_id: int, currency: str, network: str,
                          amount: float, destination: str) -> dict:
        tx = await self.create_transaction(order_id, currency, network, amount, destination)
        try:
            result = await self.provider.send(currency, network, amount, destination)
            await self.tx_repo.update_status(order_id, "confirmed", tx_hash=result.get("tx_hash"))
            return result
        except Exception as e:
            tx.error_message = str(e)
            await self.tx_repo.update_status(order_id, "failed")
            raise

    def is_valid_address(self, address: str, network: str) -> bool:
        if not address or len(address.strip()) < 10:
            return False
        if network == "TON":
            return address.startswith(("EQ", "UQ", "0:"))
        if network == "TRC20":
            return address.startswith("T")
        return True
