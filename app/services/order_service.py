from typing import Dict, Any

from sqlalchemy.orm import Session

from app.crud import crud_order, crud_product
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_in: OrderCreate, user_id: int) -> Order:
        total_price = 0
        order_items = []

        for item in order_in.items:
            product = crud_product.get(self.db, id=item.product_id)
            if not product:
                raise ValueError(f"Product with ID {item.product_id} not found")

            item_price = product.price * item.quantity
            total_price += item_price

            order_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product.price,
                "total": item_price
            })

        order_data = OrderCreate(
            address_id=order_in.address_id,
            status=OrderStatus.PENDING,
            total_amount=total_price
        )

        order = crud_order.create_with_items(
            db=self.db,
            obj_in=order_data,
            user_id=user_id,
            items=order_items
        )

        return order

    def cancel_order(self, order_id: int) -> Order:
        order = crud_order.get(self.db, id=order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        if order.status in OrderStatus.DELIVERED:
            raise ValueError(f"Cannot cancel order in {order.status} state")

        order_update = OrderUpdate(status=OrderStatus.CANCELLED)
        updated_order = crud_order.update(self.db, db_obj=order, obj_in=order_update)

        return updated_order

    def get_order_details(self, order_id: int) -> Dict[str, Any]:
        order = crud_order.get(self.db, id=order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        items_with_details = []
        for item in order.items:
            product = crud_product.get(self.db, id=item.product_id)
            items_with_details.append({
                "product_id": item.product_id,
                "product_name": product.name,
                "quantity": item.quantity,
                "unit_price": item.price,
                "total_price": item.total
            })

        return {
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "total_price": order.total_price,
            "items": items_with_details,
            "address": order.address
        }

    def update_order_status(self, order_id: int, status: OrderStatus) -> Order:
        order = crud_order.get(self.db, id=order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        if order.status == OrderStatus.CANCELLED and status != OrderStatus.CANCELLED:
            raise ValueError("Cannot change status of a cancelled order")

        if order.status == OrderStatus.DELIVERED and status != OrderStatus.DELIVERED:
            raise ValueError("Cannot change status of a delivered order")

        order_update = OrderUpdate(status=status)
        updated_order = crud_order.update(self.db, db_obj=order, obj_in=order_update)

        return updated_order
