from datetime import datetime, UTC
from enum import Enum as PyEnum
from sqlalchemy import (
    Boolean, Column, String, Float, DateTime,
    ForeignKey, Integer, Enum
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrderStatus(str, PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    address_id = Column(String, ForeignKey("address.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    delivery_time = Column(DateTime, nullable=True)
    is_paid = Column(Boolean, default=False)
    payment_method = Column(String, nullable=True)

    # Отношения
    user = relationship("User", back_populates="orders")
    address = relationship("Address")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("order.id"), nullable=False)
    product_id = Column(String, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")