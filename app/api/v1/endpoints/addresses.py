from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_address
from app.schemas.address import Address, AddressCreate, AddressUpdate
from app.schemas.user import User
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Address])
def read_addresses(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve addresses for current user.
    """
    if crud_address.is_admin(current_user):
        addresses = crud_address.get_multi(db, skip=skip, limit=limit)
    else:
        addresses = crud_address.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return addresses


@router.post("/", response_model=Address)
def create_address(
        *,
        db: Session = Depends(deps.get_db),
        address_in: AddressCreate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new address.
    """
    address = crud_address.create_with_user(
        db=db, obj_in=address_in, user_id=current_user.id
    )
    return address


@router.put("/{address_id}", response_model=Address)
def update_address(
        *,
        db: Session = Depends(deps.get_db),
        address_id: int,
        address_in: AddressUpdate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an address.
    """
    address = crud_address.get(db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    if address.user_id != current_user.id and not crud_address.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    address = crud_address.update(db, db_obj=address, obj_in=address_in)
    return address


@router.get("/{address_id}", response_model=Address)
def read_address(
        *,
        db: Session = Depends(deps.get_db),
        address_id: int,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get address by ID.
    """
    address = crud_address.get(db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    if address.user_id != current_user.id and not crud_address.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return address


@router.delete("/{address_id}", response_model=Address)
def delete_address(
        *,
        db: Session = Depends(deps.get_db),
        address_id: int,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete an address.
    """
    address = crud_address.get(db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    if address.user_id != current_user.id and not crud_address.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    address = crud_address.remove(db=db, id=address_id)
    return address
