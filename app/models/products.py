from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True)
    itemcode = Column(String(50), primary_key=True, unique=True, nullable=False)
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

    # ✅ New Fields
    reorderqty = Column(String, nullable=True)
    reorderEnabled = Column(Boolean, default=False)

    # ✅ Relationships
    items = relationship("InvoucherItem", back_populates="product")  
    outvoucher_items = relationship("OutvoucherItem", back_populates="product")
    quotation_items = relationship("QuotationItem", back_populates="product")
