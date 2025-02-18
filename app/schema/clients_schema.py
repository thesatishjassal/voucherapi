from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ClientCreate(BaseModel):
    buisnessname: str
    gst_number: Optional[str] = None
    address: str
    city: str
    state: str
    pincode: str
    Client_Name: Optional[str] = None
    client_phone: constr(min_length=10, max_length=15)
    client_email: str
    client_type: str
   
class ClientResponse(BaseModel):
    id: int
    buisnessname: str
    gst_number: str
    address: str
    city: str
    state: str
    pincode: str
    Client_Name: str
    client_phone: constr(min_length=10, max_length=15)
    client_email: str
    client_type: str

class ClientUpdate(BaseModel):
    buisnessname: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    Client_Name: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_type: Optional[str] = None

model_config = ConfigDict(from_attributes=True)
