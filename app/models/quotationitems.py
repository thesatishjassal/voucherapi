from pydantic import Field
from sqlalchemy import Column, Integer, Float, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from base import Base
from decimal import Decimal  # ✅ Use this for accurate float handling
from typing import Optional
from sqlalchemy import Float
from sqlalchemy import Text

class QuotationItem(Base):
    __tablename__ = "quotationitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))
    customercode = Column(String(100), nullable=True)
    customerdescription = Column(Text, nullable=True)
    image = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    mrp = Column(Numeric(10, 2), nullable=True)  # Changed to Numeric for precision
    netPrice = Column(Numeric(10, 2), nullable=True)  # Renamed from price
    price = Column(Numeric(10, 2), nullable=True)  # Renamed from price
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)  # Integer as per API requirement
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    amount_including_gst = Column(Numeric(10, 2), nullable=True)
    without_gst = Column(Numeric(10, 2), nullable=True)  # Changed to Numeric for precision
    gst_amount = Column(Numeric(10, 2), nullable=True)  # Changed to Numeric for precision
    amount_with_gst = Column(Numeric(10, 2), nullable=True)  # Changed to Numeric for precision
    remarks = Column(String(500), nullable=True)  # Added remarks field
    netPrice: Optional[float] = Column(Float, info={"description": "NetPrice for quotation"})

    amount = Column(Float, nullable=True)  # ✅ as Float
    # ✅ New fields
    cct = Column(String(50), nullable=True)          # Correlated Color Temperature
    beamangle = Column(String(50), nullable=True)    # Beam angle (in degrees)
    cri = Column(String(50), nullable=True)          # Color Rendering Index
    cutoutdia = Column(String(50), nullable=True)    # Cutout diameter size
    lumens = Column(String(50), nullable=True)       # Luminous flux
    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Products", back_populates="quotation_items")
    itemshistory = relationship("QuotationItemHistory", back_populates="quotationitem", cascade="all, delete-orphan")