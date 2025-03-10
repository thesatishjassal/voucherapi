from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class QuotationItem(Base):
    __tablename__ = "quotationitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))
    customercode = Column(String(100), nullable=True)
    customerDescription = Column(String(100), nullable=True)
    image = Column(String(100), nullable=True)
    itemCode = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    mrp = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)

    # ✅ Fixed Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Products", back_populates="quotation_items")
