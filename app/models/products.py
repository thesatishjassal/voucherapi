from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base  # Ensure consistency in Base usage

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True)
    itemcode = Column(String, unique=True)
    itemname = Column(String)
    description = Column(String)
    category = Column(String)
    subcategory = Column(String)
    price = Column(String)
    quantity = Column(String)
    rackcode = Column(String)
    thumbnail = Column(String, nullable=True)
    size = Column(String)
    color = Column(String)
    model = Column(String)
    brand = Column(String)

    items = relationship("InvoucherItem", back_populates="product")  # ✅ Use string reference
