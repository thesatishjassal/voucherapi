from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # assuming you have a Base class setup

class Quotation(Base):
    __tablename__ = "quotations"

    quotation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Primary key now
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
    date = Column(Date, nullable=True)  # Use Date type here
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation")
