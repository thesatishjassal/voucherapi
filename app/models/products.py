from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    itemcode = Column(String(50), nullable=False, unique=True)
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

    # Optional technical fields
    cct = Column(String, nullable=True)
    beamangle = Column(String, nullable=True)
    cutoutdia = Column(String, nullable=True)
    cri = Column(String, nullable=True)
    lumens = Column(String, nullable=True)
    watt = Column(String, nullable=True)
    in_display = Column(Boolean, nullable=True, default=True)
    created_by = Column(String(255), nullable=False, default="System")

    # Relationships
    purchaseitems = relationship("PurchaseOrderItems", back_populates="product")
    items = relationship("InvoucherItem", back_populates="product")  
    salesitems = relationship("SalesorderItems", back_populates="product")  
    outvoucher_items = relationship("OutvoucherItem", back_populates="product")
    quotation_items = relationship("QuotationItem", back_populates="product")
