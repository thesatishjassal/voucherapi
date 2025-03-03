from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from base import Base  # Ensure you're using the same Base

class OutvoucherItem(Base):
    __tablename__ = "outvoucher_items"  # Adjusted table name to reflect "Outvoucher"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("outvouchers.id"), nullable=True)  # Links to Outvoucher table
    sr_no = Column(Integer, nullable=True)  # SR NO from product info
    product_id = Column(String(50), ForeignKey("products.id"), nullable=True)  # Item Code
    item_name = Column(String(100), nullable=True)  # Item Name
    unit = Column(String(20), nullable=True)  # Unit
    rack_code = Column(String(50), nullable=True)  # Rackcode
    quantity = Column(Integer, nullable=False)  # Qty, required
    comments = Column(Text, nullable=True)  # Comments

    # Relationships
    outvoucher = relationship("Outvoucher", back_populates="items")  # Assuming Outvoucher exists
    product = relationship("Products", back_populates="items")  # Assuming Products exists