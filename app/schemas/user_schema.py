from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr  # Ensure the email is validated correctly as an email format

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # This is required to tell Pydantic to treat data like ORM models (e.g., from database rows)
