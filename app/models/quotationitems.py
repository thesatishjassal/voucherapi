from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    ForeignKey,
    Text,
    Float
)
from sqlalchemy.orm import relationship
from base import Base


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

    # ✅ Decimal-friendly columns
    mrp = Column(Numeric(10, 2), nullable=True)
    netPrice = Column(Numeric(10, 2), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)

    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)

    # Text allows longer item names
    item_name = Column(Text, nullable=True)
    unit = Column(String(20), nullable=True)

    amount_including_gst = Column(Numeric(10, 2), nullable=True)
    without_gst = Column(Numeric(10, 2), nullable=True)
    gst_amount = Column(Numeric(10, 2), nullable=True)
    amount_with_gst = Column(Numeric(10, 2), nullable=True)
    amount = Column(Float, nullable=True)
    remarks = Column(String(500), nullable=True)

    # Extra optional fields
    cct = Column(String(50), nullable=True)
    beamangle = Column(String(50), nullable=True)
    cri = Column(String(50), nullable=True)
    cutoutdia = Column(String(50), nullable=True)
    lumens = Column(String(50), nullable=True)

    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Products", back_populates="quotation_items")
