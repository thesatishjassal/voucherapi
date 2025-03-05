from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

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
    unit = Column(String)

    # ✅ Define relationships using string names to avoid circular imports
    outvoucher_items = relationship("OutvoucherItem", back_populates="product", lazy="joined")
    invoucher_items = relationship("InvoucherItem", back_populates="product", lazy="joined")
