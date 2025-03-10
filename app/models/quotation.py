from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Quotation(Base):
    __tablename__ = "quotations"

    quotation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_no = Column(String(50), nullable=False, unique=True, index=True)
    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)
    amount_including_gst = Column(Integer, nullable=True)  # ✅ lowercase
    without_gst = Column(Integer, nullable=True)          # ✅ lowercase
    gst_amount = Column(Integer, nullable=True)           # ✅ lowercase
    amount_with_gst = Column(Integer, nullable=True)      # ✅ lowercase
    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(Boolean, nullable=True)
    date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
