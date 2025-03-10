from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Products(Base):
    __tablename__ = "products"
    
    itemcode = Column(String(50), primary_key=True, unique=True, nullable=False)  # ✅ Primary key
    hsncode = Column(String, unique=True)
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

    # ✅ Relationships
    items = relationship("InvoucherItem", back_populates="product")  
    outvoucher_items = relationship("OutvoucherItem", back_populates="product")
    quotation_items = relationship("QuotationItem", back_populates="product")
