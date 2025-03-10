from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from base import Base

class Quotation(Base):
    __tablename__ = "quotations"
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, index=True, unique=True)  # Removed autoincrement
    quotation_no = Column(String(50), nullable=False, unique=True)
    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)
    amount_including_GST = Column(Integer, nullable=True)
    without_GST = Column(Integer, nullable=True)
    GST_ammount = Column(Integer, nullable=True)
    amount_withGST = Column(Integer, nullable=True)
    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(Boolean, nullable=True)
    date = Column(Date, nullable=True)  # Fixed date type
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
