from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class UserCreate(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=15) # type: ignore
    password: str

class UserLogin(BaseModel):
    phone: Optional[constr(min_length=10, max_length=15)] = None
    password: Optional[str] = None
    
class UserResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

model_config = ConfigDict(from_attributes=True)
