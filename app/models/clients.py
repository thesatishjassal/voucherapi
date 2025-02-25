# app/models/clients.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from ...base import Base  # Adjust import based on your Base location

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    businessname = Column(String(255))
    address = Column(String(255))
    gst_number = Column(String(100))
    pincode = Column(String(20))
    city = Column(String(100))
    state = Column(String(100))
    client_name = Column(String(255))
    client_phone = Column(String(15), unique=True, index=True)
    client_email = Column(String(255), nullable=True)
    client_type = Column(String(50))

    @declared_attr
    def invouchers(cls):
        return relationship("Invoucher", back_populates="client", lazy="dynamic")