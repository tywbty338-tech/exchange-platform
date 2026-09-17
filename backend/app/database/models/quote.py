from datetime import datetime, timedelta, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import Base
import uuid


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quote_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    network: Mapped[str] = mapped_column(String(20), nullable=False)
    input_amount: Mapped[float] = mapped_column(Float, nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    output_amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used: Mapped[bool] = mapped_column(default=False)

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def remaining_seconds(self) -> int:
        diff = self.expires_at - datetime.now(timezone.utc)
        return max(0, int(diff.total_seconds()))
