from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from base import Base

class InvoucherItem(Base):
    """Model for items in an invoucher."""
    __tablename__ = "invoucher_items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    voucher_id = Column(Integer, ForeignKey("invouchers.voucher_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    item_name = Column(String(100))
    unit = Column(String(20))
    rack_code = Column(String(50))
    quantity = Column(Integer, nullable=False)
    rate = Column(DECIMAL(10,2), nullable=False)
    discount_percentage = Column(DECIMAL(5,2), default=0.00)
    amount = Column(DECIMAL(12,2), nullable=False)
    comments = Column(Text)
    
    invoucher = relationship("Invoucher", back_populates="items")
    product = relationship("Products", back_populates="items")