from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id : int
    name : str
    email: EmailStr

    class Config:
        from_attributes= True