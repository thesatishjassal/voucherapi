from pydantic import BaseModel, ConfigDict, constr

class UserCreate(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=15)
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    phone: constr(min_length=10, max_length=15)
    password: str

model_config = ConfigDict(from_attributes=True)
