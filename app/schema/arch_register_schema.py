from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ArchRegisterSchema(BaseModel):

    # AUTH
    role: str = "architect"

    # STEP 1
    full_name: str
    firm_name: str
    mobile_number: str
    email: EmailStr
    date_of_birth: date
    profession: str
    marital_status: str
    anniversary_date: Optional[date] = None

    # STEP 2
    account_holder_name: str
    bank_name: str
    account_number: str
    ifsc_code: str
    upi_id: Optional[str] = None

    class Config:
        orm_mode = True


# ── UPDATE SCHEMAS ──────────────────────────────────────────

class UpdatePersonalSchema(BaseModel):
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    marital_status: Optional[str] = None


class UpdateProfessionalSchema(BaseModel):
    profession: Optional[str] = None
    firm_name: Optional[str] = None


class UpdateBankSchema(BaseModel):
    bank_name: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    upi_id: Optional[str] = None