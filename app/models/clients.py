from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    businessname = Column(String(255), nullable=True)  # ✅ Optional
    address = Column(String(255), nullable=True)       # ✅ Optional
    gst_number = Column(String(100), nullable=True)     # ✅ Optional
    pincode = Column(String(20), nullable=True)         # ✅ Optional
    city = Column(String(100))
    state = Column(String(100))
    client_name = Column(String(255), nullable=True)    # already optional
    client_phone = Column(String(15), unique=True, index=True)
    client_email = Column(String(255), nullable=True)   # ✅ Optional
    client_type = Column(String(50))

    quotations = relationship("Quotation", back_populates="client")  
    invouchers = relationship("Invoucher", back_populates="client")
    outvouchers = relationship("Outvoucher", back_populates="client")
    salesorder = relationship("SalesOrder", back_populates="client")  
