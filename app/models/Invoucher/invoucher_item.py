from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base  # Adjust the import based on your project structure

class Product(Base):  # Renamed to singular form for consistency
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True)
    item_code = Column(String, unique=True)
    item_name = Column(String)
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

    # Use a string reference for the related class
    invoucher = relationship("Invoucher", back_populates="items")
    product = relationship("Product", back_populates="items")