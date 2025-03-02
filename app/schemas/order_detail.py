from pydantic import BaseModel


class OrderDetailBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailInDBBase(OrderDetailBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True


class OrderDetail(OrderDetailInDBBase):
    pass
