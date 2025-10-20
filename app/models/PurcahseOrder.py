from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class PurchaseOrder(Base):
    __tablename__ = "purchaseorders"

    purchaseorder_id = Column(Integer, primary_key=True, index=True)
    purchaseorder_no = Column(String(50), unique=True, nullable=False)
    purchaseperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)
    amount_including_gst = Column(Integer, nullable=True)
    without_gst = Column(Integer, nullable=True)
    gst_amount = Column(Integer, nullable=True)
    amount_with_gst = Column(Integer, nullable=True)
    remarks = Column(String(100), nullable=True)
    status = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # New fields
    payment_method = Column(String(50), nullable=True)  # Cash, Card, UPI
    freight = Column(String(20), nullable=True)        # Paid or To Pay
    issue_slip_no = Column(String(50), nullable=True)

    # Relationships using string names
    client = relationship("Client", back_populates="purchaseorder")
    purchaseitems = relationship("PurchaseOrderItems", back_populates="purchaseorder", cascade="all, delete-orphan")
