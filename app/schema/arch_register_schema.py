from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ArchRegisterSchema(BaseModel):

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