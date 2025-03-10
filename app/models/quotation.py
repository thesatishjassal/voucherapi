from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Quotation(Base):
    __tablename__ = "quotations"

    quotation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_no = Column(String(50), nullable=False, unique=True, index=True)  # Ensuring fast query
    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)
    amount_including_GST = Column(Integer, nullable=True)
    without_GST = Column(Integer, nullable=True)
    GST_amount = Column(Integer, nullable=True)  # ✅ Correct spelling
    amount_with_GST = Column(Integer, nullable=True)  
    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(Boolean, nullable=True)
    date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
