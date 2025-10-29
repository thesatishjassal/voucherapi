from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ClientCreate(BaseModel):
    businessname: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None
    city: str
    state: str
    pincode: Optional[str] = None
    client_name: Optional[str] = None
    client_phone: constr(min_length=10, max_length=15)
    client_email: Optional[str] = None
    client_type: str
    # ✅ New field
    created_by: str

class ClientResponse(BaseModel):
    id: int
    businessname: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None
    city: str
    state: str
    pincode: Optional[str] = None
    client_name: Optional[str] = None
    client_phone: constr(min_length=10, max_length=15)
    client_email: Optional[str] = None
    client_type: str
    # ✅ New field
    created_by: str

class ClientUpdate(BaseModel):
    businessname: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_type: Optional[str] = None
    # ✅ Optional update field
    created_by: Optional[str] = None

model_config = ConfigDict(from_attributes=True)
