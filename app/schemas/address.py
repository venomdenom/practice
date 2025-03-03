from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: str
    country: str = "Россия"
    is_default: bool = False


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None


class AddressInDBBase(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Address(AddressInDBBase):
    pass
