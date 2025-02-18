from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py

class Clients(Base):
    __tablename__ = "clients"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed
    
    id = Column(Integer, primary_key=True, index=True)
    buisnessname = Column(String)
    address = Column(String)
    gst_number = Column(String)
    pincode = Column(String)
    city = Column(String)
    state= Column(String)
    Client_Name = Column(String)
    client_phone = Column(String(15), unique=True, index=True)  # E.164 format max length 15
    client_email = Column(String)
    client_type = Column(String)

    def __repr__(self):
        return f"<Clients (id={self.id}, buisnessname={self.buisnessname}, address={self.address}, gst_number={self.gst_number}, pincode={self.pincode},city={self.city}, state={self.state}, Client_Name={self.Client_Name}, client_phone={self.client_phone},  client_email={self. client_email},  client_type={self. client_type})>"