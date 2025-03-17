from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base


class QuotationItemHistory(Base):
    __tablename__ = "quotationitemhistory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_item_id = Column(Integer, ForeignKey("quotationitems.id"), nullable=False)
    quotation_id = Column(Integer, nullable=True)
    product_id = Column(String(50), nullable=True)
    customercode = Column(String(100), nullable=True)
    customerdescription = Column(String(100), nullable=True)
    image = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    mrp = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    discount = Column(Integer, nullable=True)
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    edited_at = Column(DateTime, default=datetime.utcnow)
    edited_by = Column(String(100), nullable=True)
    action = Column(String(50), nullable=True)

    quotationitem = relationship("QuotationItem", back_populates="itemshistory")