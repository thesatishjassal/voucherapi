from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from base import Base

class OutvoucherItem(Base):
    __tablename__ = "outvoucher_items"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("outvouchers.id"), nullable=True)
    sr_no = Column(Integer, nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)  # 🔹 Changed from String(50) to Integer
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    rack_code = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)

    # Relationships
    outvoucher = relationship("Outvoucher", back_populates="items")
    product = relationship("Products", back_populates="outvoucher_items")
