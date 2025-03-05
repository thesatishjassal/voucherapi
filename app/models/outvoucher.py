from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, Text
from sqlalchemy.orm import relationship
from base import Base

class Outvoucher(Base):
    __tablename__ = "outvouchers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, nullable=True)
    voucher_no = Column(String(50), nullable=False, unique=True)
    issue_slip_no = Column(String(50), nullable=True)
    sale_order_no = Column(String(50), nullable=True)
    transport = Column(String(100), nullable=True)
    vehicle_no = Column(String(50), nullable=True)
    number_of_packages = Column(Integer, nullable=True)
    ordered_by = Column(String(100), nullable=True)
    sales_person = Column(String(100), nullable=True)
    freight_amount = Column(DECIMAL(10, 2), nullable=True, default=0.00)
    remarks = Column(Text, nullable=True)
    receiver_name = Column(String(100), nullable=True)
    mobile_number = Column(String(20), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # ✅ Fix Relationships
    client = relationship("Client", back_populates="outvouchers")
    items = relationship("OutvoucherItem", back_populates="outvoucher") 
