from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True, nullable=False)
    item_code = Column(String, unique=True, nullable=False)
    item_name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    sub_category = Column(String)
    price = Column(String)
    quantity = Column(String)
    rack_code = Column(String)
    thumbnail = Column(String, nullable=True)
    size = Column(String)
    color = Column(String)
    model = Column(String)
    brand = Column(String)

    # Define the relationship without referencing the class directly
    invoucher_items = relationship("InvoucherItem", back_populates="product")
