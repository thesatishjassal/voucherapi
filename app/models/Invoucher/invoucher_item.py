# invoucher_item.py
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from ....base import Base  # Adjust import based on your Base location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .invoucher import Invoucher
    from ..products import Product

class InvoucherItem(Base):
    __tablename__ = "invoucher_items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    voucher_id = Column(Integer, ForeignKey("invouchers.voucher_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    item_name = Column(String(100))
    unit = Column(String(20))
    rack_code = Column(String(50))
    quantity = Column(Integer, nullable=False)
    rate = Column(DECIMAL(10, 2), nullable=False)
    discount_percentage = Column(DECIMAL(5, 2), default=0.00)
    amount = Column(DECIMAL(12, 2), nullable=False)
    comments = Column(Text)

    invoucher = relationship("Invoucher", back_populates="items")
    product = relationship("Product", back_populates="items")