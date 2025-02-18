from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ClientCreate(BaseModel):
    buisnessname: str
    gst_number: Optional[str] = None
    Address: str
    City: str
    State: str
    pincode: str
    Client_Name: Optional[str] = None
    client_phone: constr(min_length=10, max_length=15)
    client_email: str
    client_type: str
   
class ClientResponse(BaseModel):
    id: int
    buisnessname: str
    gst_number: str
    Address: str
    City: str
    State: str
    pincode: str
    Client_Name: str
    client_phone: constr(min_length=10, max_length=15)
    client_email: str
    client_type: str

class ClientUpdate(BaseModel):
    buisnessname: Optional[str] = None
    gst_number: Optional[str] = None
    Address: Optional[str] = None
    pincode: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Client_Name: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_type: Optional[str] = None

model_config = ConfigDict(from_attributes=True)
