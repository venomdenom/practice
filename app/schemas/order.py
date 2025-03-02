from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.models.order import OrderStatus
from app.schemas.order_detail import OrderDetail, OrderDetailCreate


class OrderBase(BaseModel):
    address_id: int
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    delivery_fee: float = 0.0
    estimated_delivery_time: Optional[datetime] = None
    special_instructions: Optional[str] = None


class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]


class OrderUpdate(BaseModel):
    address_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[OrderStatus] = None
    delivery_fee: Optional[float] = None
    estimated_delivery_time: Optional[datetime] = None
    special_instructions: Optional[str] = None


class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    order_details: List[OrderDetail] = []
