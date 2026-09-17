from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.admin import Admin


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_admin(self, telegram_id: int) -> bool:
        result = await self.session.execute(select(Admin).where(Admin.telegram_id == telegram_id, Admin.active == True))
        return result.scalar_one_or_none() is not None
