from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Invoucher.invoucher_item import InvoucherItem

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True, nullable=False)
    itemCode = Column(String, unique=True, nullable=False)
    itemName = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    subCategory = Column(String)
    price = Column(String)
    quantity = Column(String)
    rackCode = Column(String)
    thumbnail = Column(String, nullable=True)
    size = Column(String)
    color = Column(String)
    model = Column(String)
    brand = Column(String)

    # Forward declaration of the relationship
    items = relationship("InvoucherItem", back_populates="product")
