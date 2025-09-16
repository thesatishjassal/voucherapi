from sqlalchemy import Column, DateTime, Integer, String, Boolean, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

class Quotation(Base):
    __tablename__ = 'quotations'

    quotation_id = Column(Integer, primary_key=True, index=True)
    quotation_no = Column(String(50), unique=True, nullable=False)
    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)
    amount_including_gst = Column(Integer, nullable=True)
    without_gst = Column(Integer, nullable=True)
    gst_amount = Column(Integer, nullable=True)
    amount_with_gst = Column(Integer, nullable=True)
    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())  # ✅

    # Relationships
    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
 