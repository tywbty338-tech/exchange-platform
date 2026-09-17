from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    QUOTE_CREATED = "QUOTE_CREATED"
    WAITING_PAYMENT = "WAITING_PAYMENT"
    PAYMENT_PROCESSING = "PAYMENT_PROCESSING"
    PAYMENT_CONFIRMED = "PAYMENT_CONFIRMED"
    WAITING_WALLET = "WAITING_WALLET"
    WALLET_CONFIRMED = "WALLET_CONFIRMED"
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    TRANSFER_FAILED = "TRANSFER_FAILED"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    input_currency: Mapped[str] = mapped_column(String(10), nullable=False, default="IQD")
    input_amount: Mapped[float] = mapped_column(Float, nullable=False)
    output_currency: Mapped[str] = mapped_column(String(10), nullable=False)
    output_amount: Mapped[float] = mapped_column(Float, nullable=False)
    network: Mapped[str] = mapped_column(String(20), nullable=False)
    exchange_rate: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    wallet_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default=OrderStatus.CREATED.value)
    quote_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="orders", lazy="selectin")
    payment = relationship("Payment", back_populates="order", uselist=False, lazy="selectin")
    transactions = relationship("Transaction", back_populates="order", lazy="selectin")
