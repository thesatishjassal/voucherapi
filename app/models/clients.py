from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py

class Clients(Base):
    __tablename__ = "clients"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed
    
    id = Column(Integer, primary_key=True, index=True)
    BuisnessName = Column(String)
    Address = Column(String)
    GST_Number = Column(String)
    Pincode = Column(String)
    City = Column(String)
    State = Column(String)
    Client_Name = Column(String)
    Client_Phone = Column(String(15), unique=True, index=True)  # E.164 format max length 15
    Client_Email = Column(String)
    Client_Type = Column(String)

    def __repr__(self):
        return f"<Clients (id={self.id}, BuisnessName={self.BuisnessName}, Address={self.Address}, GST_Number={self.GST_Number}, Pincode={self.Pincode},City={self.City}, State={self.State}, Client_Name={self.Client_Name}, Client_Phone={self.Client_Phone},  Client_Email={self. Client_Email},  Client_Type={self. Client_Type})>"
