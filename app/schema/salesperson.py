from pydantic import BaseModel, EmailStr

class SalesPersonCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    architecture_name: str
    company_name: str


class SalesPersonUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    architecture_name: str | None = None
    company_name: str | None = None


class SalesPersonResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    architecture_name: str
    company_name: str

    class Config:
        from_attributes = True