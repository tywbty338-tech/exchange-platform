from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base


class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    network: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    fee_type: Mapped[str] = mapped_column(String(20), nullable=False, default="fixed")
    fee_value: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    min_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    max_amount: Mapped[float] = mapped_column(Float, nullable=False, default=999999999)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
