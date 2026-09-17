from pydantic import BaseModel, Field
from datetime import datetime


class RateResponse(BaseModel):
    currency: str
    network: str
    rate: float
    fee_type: str
    fee_value: float
    min_amount: float
    max_amount: float
    active: bool
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class QuoteRequest(BaseModel):
    currency: str
    network: str
    input_amount: float


class QuoteResponse(BaseModel):
    quote_id: str
    currency: str
    network: str
    input_amount: float
    rate: float
    fee: float
    output_amount: float
    expires_at: datetime
    remaining_seconds: int


class OrderCreate(BaseModel):
    quote_id: str


class OrderResponse(BaseModel):
    id: int
    order_number: str
    input_currency: str
    input_amount: float
    output_currency: str
    output_amount: float
    network: str
    exchange_rate: float
    fee: float
    wallet_address: str | None
    status: str
    created_at: datetime | None = None
    completed_at: datetime | None = None

    class Config:
        from_attributes = True


class WalletCreate(BaseModel):
    currency: str
    network: str
    address: str
    label: str | None = None


class WalletResponse(BaseModel):
    id: int
    currency: str
    network: str
    address: str
    label: str | None
    is_default: bool

    class Config:
        from_attributes = True


class WalletAddressUpdate(BaseModel):
    wallet_address: str


class AdminRateUpdate(BaseModel):
    rate: float | None = None
    fee_type: str | None = None
    fee_value: float | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    active: bool | None = None


class AdminRateConfirm(BaseModel):
    old_rate: float
    new_rate: float
    currency: str
    network: str


class StatsResponse(BaseModel):
    total_users: int
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_volume: float


class ApiResponse(BaseModel):
    success: bool = True
    data: dict | None = None
    error: dict | None = None
