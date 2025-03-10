# ✅ Define Quotation after Client
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Quotation(Base):
    __tablename__ = "quotations"
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    date = Column(Integer, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
