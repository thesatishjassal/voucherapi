from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class QuotationBase(BaseModel):
    id: Optional[int] = None
    quotation_id: Optional[int] = None  # Made optional
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_GST: Optional[int] = None
    without_GST: Optional[int] = None
    GST_ammount: Optional[int] = None
    amount_withGST: Optional[int] = None
    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[bool] = None
    date: Optional[date] = None  # Keep date for compatibility
    client_id: int

class QuotationCreate(QuotationBase):
    pass

class QuotationUpdate(QuotationBase):
    pass

class Quotation(QuotationBase):
    model_config = ConfigDict(from_attributes=True)  # ORM compatibility
