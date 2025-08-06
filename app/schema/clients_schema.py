from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ClientCreate(BaseModel):
    businessname: Optional[str] = None  # ✅ Optional
    gst_number: Optional[str] = None    # ✅ Optional
    address: Optional[str] = None       # ✅ Optional
    city: str
    state: str
    pincode: Optional[str] = None       # ✅ Optional
    client_name: Optional[str] = None
    client_phone: constr(min_length=10, max_length=15)
    client_email: Optional[str] = None  # ✅ Optional
    client_type: str

class ClientResponse(BaseModel):
    id: int
    businessname: Optional[str] = None  # ✅ Optional
    gst_number: Optional[str] = None    # ✅ Optional
    address: Optional[str] = None       # ✅ Optional
    city: str
    state: str
    pincode: Optional[str] = None       # ✅ Optional
    client_name: str
    client_phone: constr(min_length=10, max_length=15)
    client_email: Optional[str] = None  # ✅ Optional
    client_type: str

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

model_config = ConfigDict(from_attributes=True)
