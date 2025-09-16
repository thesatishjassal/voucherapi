from datetime import datetime, date          # ✅ import the class
from pydantic import BaseModel, ConfigDict
from typing import Optional

class QuotationBase(BaseModel):
    quotation_id: Optional[int] = None
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None
    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None
    client_id: int
    created_at: Optional[datetime] = None    # ✅ correct type

class QuotationCreate(BaseModel):
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None
    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None
    client_id: int

class QuotationUpdate(QuotationBase):
    pass

class Quotation(QuotationBase):
    model_config = ConfigDict(from_attributes=True)
