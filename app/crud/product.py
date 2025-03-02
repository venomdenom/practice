from typing import List, Optional, Dict, Any, Union, Type

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        """
        Get a product by name.
        """
        return db.query(Product).filter(Product.name == name).first()

    def get_by_category(
            self, db: Session, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Type[Product]]:
        """
        Get products by category.
        """
        return (
            db.query(Product)
            .filter(Product.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_available_products(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Type[Product]]:
        """
        Get products that are in stock.
        """
        return (
            db.query(Product)
            .filter(Product.stock_quantity > 0)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_stock(
            self, db: Session, *, product_id: int, quantity_change: int
    ) -> Product:
        """
        Update product stock quantity.
        """
        product = self.get(db, id=product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        product.stock_quantity += quantity_change

        # Ensure stock quantity doesn't go below 0
        if product.stock_quantity < 0:
            product.stock_quantity = 0

        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def search_products(
            self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Type[Product]]:
        """
        Search products by name or description.
        """
        search_pattern = f"%{query}%"
        return (
            db.query(Product)
            .filter(
                (Product.name.ilike(search_pattern)) |
                (Product.description.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_product = CRUDProduct(Product)
