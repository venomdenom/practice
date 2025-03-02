from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_order
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.schemas.user import User
from app.api.deps import get_current_active_user
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[Order])
def read_orders(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    if crud_order.is_admin(current_user):
        orders = crud_order.get_multi(db, skip=skip, limit=limit)
    else:
        orders = crud_order.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return orders


@router.post("/", response_model=Order)
def create_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: OrderCreate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    order_service = OrderService(db)
    order = order_service.create_order(order_in=order_in, user_id=current_user.id)
    return order


@router.put("/{order_id}", response_model=Order)
def update_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: int,
        order_in: OrderUpdate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an order.
    """
    order = crud_order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and not crud_order.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    order = crud_order.update(db, db_obj=order, obj_in=order_in)
    return order


@router.get("/{order_id}", response_model=Order)
def read_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: int,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get order by ID.
    """
    order = crud_order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and not crud_order.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return order


@router.delete("/{order_id}", response_model=Order)
def cancel_order(
        *,
        db: Session = Depends(deps.get_db),
        order_id: int,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Cancel an order.
    """
    order = crud_order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and not crud_order.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    order_service = OrderService(db)
    order = order_service.cancel_order(order_id=order_id)
    return order
