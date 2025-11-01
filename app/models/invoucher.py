from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Text, CheckConstraint, DateTime, func
from sqlalchemy.orm import relationship
from base import Base  # Ensure consistency in Base usage

class Invoucher(Base):
    __tablename__ = "invouchers"

    id = Column(Integer, primary_key=True)
    voucher_id = Column(Integer, unique=True, index=True)  
    voucher_number = Column(String(20), unique=True, nullable=False)
    transaction_type = Column(String(50), nullable=False, default="Transfer")
    voucher_date = Column(Date, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))
    invoice_number = Column(String(20))
    invoice_date = Column(Date)
    mode_of_transport = Column(String(50))
    number_of_packages = Column(Integer)
    freight_status = Column(String(20), CheckConstraint("freight_status IN ('Paid', 'Unpaid')"))
    total_amount = Column(DECIMAL(12, 2), default=0.00)
    remarks = Column(Text)
    gst_option = Column(String(20), CheckConstraint("gst_option IN ('Include', 'Exclude')"), default="Include")  # New column
    gst_percentage = Column(DECIMAL(5, 2), default=0.00)  # New column
    gst_amount = Column(DECIMAL(12, 2), default=0.00)  # New column
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=False, default="System")

    client = relationship("Client", back_populates="invouchers")
    items = relationship("InvoucherItem", back_populates="invoucher")