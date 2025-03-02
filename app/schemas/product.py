from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: Optional[bool] = True
    stock_quantity: Optional[int] = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None


class ProductRead(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
