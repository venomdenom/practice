from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_product
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.schemas.user import User
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[Product])
def read_products(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve products.
    """
    products = crud_product.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=Product)
def create_product(
        *,
        db: Session = Depends(deps.get_db),
        product_in: ProductCreate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    if not crud_product.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="Not enough permissions to create product"
        )
    product = crud_product.create(db, obj_in=product_in)
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
        *,
        db: Session = Depends(deps.get_db),
        product_id: int,
        product_in: ProductUpdate,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not crud_product.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    product = crud_product.update(db, db_obj=product, obj_in=product_in)
    return product


@router.get("/{product_id}", response_model=Product)
def read_product(
        *,
        db: Session = Depends(deps.get_db),
        product_id: int,
) -> Any:
    """
    Get product by ID.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", response_model=Product)
def delete_product(
        *,
        db: Session = Depends(deps.get_db),
        product_id: int,
        current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a product.
    """
    product = crud_product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not crud_product.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    product = crud_product.remove(db=db, id=product_id)
    return product
