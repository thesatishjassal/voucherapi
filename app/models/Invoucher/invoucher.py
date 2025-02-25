from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Text, CheckConstraint
from sqlalchemy.orm import relationship
from base import Base

class Invoucher(Base):
    __tablename__ = "invouchers"

    voucher_id = Column(Integer, primary_key=True, index=True)
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

    client = relationship("Clients", back_populates="invouchers")
    items = relationship("InvoucherItem", back_populates="invoucher")
