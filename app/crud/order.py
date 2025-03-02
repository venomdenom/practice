from typing import List, Optional, Dict, Any, Union, Type

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi_by_user(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Type[Order]]:
        """
        Get multiple orders by user ID.
        """
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_items(
            self, db: Session, *, obj_in: OrderCreate, user_id: str, items: List[Dict[str, Any]]
    ) -> Order:
        """
        Create a new order with order items.
        """
        order_data = obj_in.dict(exclude={"items"})
        db_obj = Order(**order_data, user_id=user_id)
        db.add(db_obj)
        db.flush()  # Get the order ID without committing

        # Create order items
        for item_data in items:
            order_item = OrderItem(
                order_id=db_obj.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["price"],
            )
            db.add(order_item)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_orders_by_status(
            self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Type[Order]]:
        """
        Get orders by status.
        """
        return (
            db.query(Order)
            .filter(Order.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent_orders(
            self, db: Session, *, days: int = 7, skip: int = 0, limit: int = 100
    ) -> List[Type[Order]]:
        """
        Get orders created in the last X days.
        """
        import datetime
        date_from = datetime.datetime.now() - datetime.timedelta(days=days)
        return (
            db.query(Order)
            .filter(Order.created_at >= date_from)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_order = CRUDOrder(Order)
