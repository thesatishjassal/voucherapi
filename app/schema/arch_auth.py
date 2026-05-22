from pydantic import BaseModel, EmailStr

class ArchLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ArchTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"