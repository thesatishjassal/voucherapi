from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ClientCreate(BaseModel):
    BuisnessName: str
    GST_Number: Optional[str] = None
    Address: str
    City: str
    State: str
    Pincode: str
    Client_Name: Optional[str] = None
    Client_Phone: constr(min_length=10, max_length=15)
    Client_Email: str
    Client_Type: str
   
class ClientResponse(BaseModel):
    id: int
    BuisnessName: str
    GST_Number: str
    Address: str
    City: str
    State: str
    Pincode: str
    Client_Name: str
    Client_Phone: constr(min_length=10, max_length=15)
    Client_Email: str
    Client_Type: str

class ClientUpdate(BaseModel):
    BuisnessName: Optional[str] = None
    GST_Number: Optional[str] = None
    Address: Optional[str] = None
    Pincode: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Client_Name: Optional[str] = None
    Client_Phone: Optional[str] = None
    Client_Email: Optional[str] = None
    Client_Type: Optional[str] = None

model_config = ConfigDict(from_attributes=True)
