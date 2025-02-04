from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=15)
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    phone: str

class Config:
    orm_mode = True