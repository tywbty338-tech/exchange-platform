from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import get_settings

settings = get_settings()

if settings.database_url.startswith("sqlite"):
    engine = create_async_engine(settings.database_url, echo=False)
else:
    engine = create_async_engine(settings.database_url, echo=False, pool_size=10, max_overflow=20)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    from app.database.models import user, order, payment, rate, quote, transaction, wallet, admin, setting, audit_log  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


from app.database.models.base import Base
