from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    buisnessname = Column(String(255))  # Note: Typo "buisnessname" → should be "businessname"
    address = Column(String(255))
    gst_number = Column(String(100))
    pincode = Column(String(20))
    city = Column(String(100))
    state = Column(String(100))
    client_name = Column(String(255))
    client_phone = Column(String(15), unique=True, index=True)
    client_email = Column(String(255), nullable=True)
    client_type = Column(String(50))

    # Relationships
    invouchers = relationship("Invoucher", back_populates="client")
    outvouchers = relationship("Outvoucher", back_populates="client")

    def __repr__(self):
        return f"<Clients (id={self.id}, businessname={self.businessname}, address={self.address}, gst_number={self.gst_number}, pincode={self.pincode}, city={self.city}, state={self.state}, client_name={self.client_name}, client_phone={self.client_phone}, client_email={self.client_email}, client_type={self.client_type})>"