from typing import List, Optional, Dict, Any, Union, Type

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    def get_multi_by_user(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Type[Address]]:
        """
        Get multiple addresses by user ID.
        """
        return (
            db.query(Address)
            .filter(Address.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
            self, db: Session, *, obj_in: AddressCreate, user_id: str
    ) -> Address:
        """
        Create a new address for a specific user.
        """
        obj_in_data = obj_in.dict()
        db_obj = Address(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_default_address(self, db: Session, *, user_id: int) -> Optional[Address]:
        """
        Get the default address for a user.
        """
        return (
            db.query(Address)
            .filter(Address.user_id == user_id, Address.is_default == True)
            .first()
        )

    def set_as_default(self, db: Session, *, address_id: int, user_id: int) -> Address:
        """
        Set an address as default for a user, and clear default status from others.
        """
        # Clear default status from all user's addresses
        user_addresses = self.get_multi_by_user(db, user_id=user_id)
        for address in user_addresses:
            address.is_default = False
            db.add(address)

        # Set the specified address as default
        address = self.get(db, id=address_id)
        if not address or address.user_id != user_id:
            raise ValueError("Address not found or doesn't belong to the user")

        address.is_default = True
        db.add(address)
        db.commit()
        db.refresh(address)
        return address


crud_address = CRUDAddress(Address)
