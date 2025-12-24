from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from base import Base

class OutvoucherItem(Base):
    __tablename__ = "outvoucheritems"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("outvouchers.id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))
    item_name =  Column(Text, nullable=True)
    unit = Column(String(20), nullable=True)
    rack_code = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    
    amount_including_gst = Column(Integer, nullable=True)
    without_gst = Column(Integer, nullable=True)
    gst_amount = Column(Integer, nullable=True)
    amount_with_gst = Column(Integer, nullable=True)
    
    outvoucher = relationship("Outvoucher", back_populates="items")
    product = relationship("Products", back_populates="outvoucher_items")
