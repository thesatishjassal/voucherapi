from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base  # Use centralized Base

class Client(Base):  # Renamed from Clients → Client
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    buisnessname = Column(String(255))  # Fixed typo (buisnessname → buisnessname)
    address = Column(String(255))
    gst_number = Column(String(100))
    pincode = Column(String(20))
    city = Column(String(100))
    state = Column(String(100))
    client_name = Column(String(255))
    client_phone = Column(String(15), unique=True, index=True)
    client_email = Column(String(255), nullable=True)
    client_type = Column(String(50))

    invouchers = relationship("Invoucher", back_populates="client")  # String reference
