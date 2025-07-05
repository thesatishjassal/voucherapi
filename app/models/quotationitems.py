from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class QuotationItem(Base):
    __tablename__ = "quotationitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))
    customercode = Column(String(100), nullable=True)
    customerdescription = Column(String(100), nullable=True)  # ✅ Lowercase
    image = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)  # ✅ Lowercase
    brand = Column(String(100), nullable=True)
    mrp = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    amount_including_gst = Column(Numeric(10, 2), nullable=True)

    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Products", back_populates="quotation_items")
    itemshistory = relationship("QuotationItemHistory", back_populates="quotationitem", cascade="all, delete-orphan")
