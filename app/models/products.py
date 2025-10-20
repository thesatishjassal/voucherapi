from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    # hsncode = Column(String, unique=True)
    itemcode = Column(String(50), nullable=False)
    itemname = Column(String)
    description = Column(String)
    category = Column(String)
    subcategory = Column(String)
    price = Column(Float, nullable=True)
    quantity = Column(Integer)
    rackcode = Column(String)
    thumbnail = Column(String, nullable=True)
    size = Column(String)
    color = Column(String)
    model = Column(String)
    brand = Column(String)
    unit = Column(String)
    reorderqty = Column(Integer, nullable=True)

    # ✅ New optional fields (text type)
    cct = Column(String, nullable=True)
    beamangle = Column(String, nullable=True)
    cutoutdia = Column(String, nullable=True)
    cri = Column(String, nullable=True)
    lumens = Column(String, nullable=True)
    watt = Column(String, nullable=True)
    # ✅ Optional field
    in_display = Column(Boolean, nullable=True, default=True)

    # Relationships
    items = relationship("InvoucherItem", back_populates="product")  
    salesitems = relationship("SalesorderItems", back_populates="product")  
    # purchaseitems = relationship("SalesorderItems", back_populates="product")  
    outvoucher_items = relationship("OutvoucherItem", back_populates="product")
    quotation_items = relationship("QuotationItem", back_populates="product")
