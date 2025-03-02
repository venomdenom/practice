from app.crud.base import CRUDBase
from app.crud.user import CRUDUser, crud_user
from app.crud.product import CRUDProduct, crud_product
from app.crud.order import CRUDOrder, crud_order
from app.crud.address import CRUDAddress, crud_address

__all__ = ["CRUDBase", "CRUDUser", "crud_user", "CRUDProduct", "crud_product",
           "CRUDOrder", "crud_order", "CRUDAddress", "crud_address"]