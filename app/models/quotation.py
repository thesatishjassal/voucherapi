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

    # ✅ ADD (SAFE)
    gst_type = Column(String(10), nullable=True, default="include")   # include / exclude
    gst_percentage = Column(Integer, nullable=True, default=0)

    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(String, nullable=True)
    date = Column(Date, nullable=True)

    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=False, default="System")

    # ✅ EXISTING DISCOUNT FIELDS (UNCHANGED)
    additional_discount_percentage = Column(Integer, nullable=True, default=0)
    additional_discount_amount = Column(Integer, nullable=True, default=0)
    amount_after_discount = Column(Integer, nullable=True)

    # ✅ ADD (FINAL OUTPUT FIELD)
    final_amount = Column(Integer, nullable=True)

    # Relationships
    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")