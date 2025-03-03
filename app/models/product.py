from datetime import datetime, UTC
from sqlalchemy import Boolean, Column, String, Float, Text, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    category = Column(String, index=True, nullable=True)
    is_available = Column(Boolean(), default=True)
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    order_items = relationship("OrderItem", back_populates="product")
