import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.payment_repo import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentProvider(ABC):
    @abstractmethod
    async def initiate_payment(self, order_id: int, amount: float, phone: str) -> dict:
        pass

    @abstractmethod
    async def check_status(self, provider_reference: str) -> str:
        pass


class MockPaymentProvider(PaymentProvider):
    async def initiate_payment(self, order_id: int, amount: float, phone: str) -> dict:
        logger.info(f"[MOCK] Payment: order={order_id}, amount={amount}, phone={phone}")
        return {"provider_reference": f"MOCK-{order_id}", "status": "confirmed"}

    async def check_status(self, provider_reference: str) -> str:
        return "confirmed"


class ManualPaymentProvider(PaymentProvider):
    async def initiate_payment(self, order_id: int, amount: float, phone: str) -> dict:
        return {"provider_reference": f"MANUAL-{order_id}", "status": "pending"}

    async def check_status(self, provider_reference: str) -> str:
        return "pending"


class AsiaCellProvider(PaymentProvider):
    async def initiate_payment(self, order_id: int, amount: float, phone: str) -> dict:
        raise NotImplementedError("AsiaCell provider not yet configured")

    async def check_status(self, provider_reference: str) -> str:
        raise NotImplementedError("AsiaCell provider not yet configured")


def get_payment_provider(provider_name: str = "mock") -> PaymentProvider:
    providers = {"mock": MockPaymentProvider, "manual": ManualPaymentProvider, "asiacell": AsiaCellProvider}
    return providers.get(provider_name, MockPaymentProvider)()


class PaymentService:
    def __init__(self, session: AsyncSession, provider_name: str = "mock"):
        self.session = session
        self.repo = PaymentRepository(session)
        self.provider = get_payment_provider(provider_name)

    async def create_payment(self, order_id: int, amount: float, currency: str = "IQD"):
        return await self.repo.create(order_id=order_id, provider=self.provider.__class__.__name__,
                                      amount=amount, currency=currency, status="pending")

    async def initiate_payment(self, order_id: int, amount: float, phone: str):
        result = await self.provider.initiate_payment(order_id, amount, phone)
        await self.repo.update_status(order_id, result.get("status", "pending"),
                                      provider_reference=result.get("provider_reference"))
        return result

    async def update_status(self, order_id: int, status: str, provider_reference: str | None = None):
        return await self.repo.update_status(order_id, status, provider_reference)
