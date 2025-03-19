from pydantic import BaseModel, ConfigDict, constr

class UserCreate(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=15)
    password: str
    role: str  # Added role field

class UserLogin(BaseModel):
    phone: constr(min_length=10, max_length=15)
    password: str  # Raw password entered by the user
    
class UserResponse(BaseModel):
    id: int
    name: str
    phone: constr(min_length=10, max_length=15)
    password: str
    role: str  # Added role field

    model_config = ConfigDict(from_attributes=True)