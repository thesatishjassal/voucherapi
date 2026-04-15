from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, func, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Quotation(Base):
    __tablename__ = 'quotations'

    quotation_id = Column(Integer, primary_key=True, index=True)
    quotation_no = Column(String(50), unique=True, nullable=False)
    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)

    amount_including_gst = Column(Numeric(12, 2), nullable=True)
    without_gst = Column(Numeric(12, 2), nullable=True)
    gst_amount = Column(Numeric(12, 2), nullable=True)
    amount_with_gst = Column(Numeric(12, 2), nullable=True)

    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(String(20), nullable=True)
    date = Column(Date, nullable=True)

    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=False, default="System")

    # ✅ FIXED DISCOUNT FIELDS
    additional_discount_percentage = Column(Integer, nullable=False, default=0)
    additional_discount_amount = Column(Numeric(12, 2), nullable=False, default=0)
    amount_after_discount = Column(Numeric(12, 2), nullable=False, default=0)
    gst_percentage = Column(Integer, nullable=False, default=18)
    gst_type = Column(String(10), nullable=False, default="include")
        # Relationships
    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")