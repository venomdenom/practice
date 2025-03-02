from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Address(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Russia")
    is_default = Column(Boolean, default=False)
    apartment = Column(String, nullable=True)
    floor = Column(String, nullable=True)
    entrance = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    user = relationship("User", back_populates="addresses")