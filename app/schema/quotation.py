from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import Optional

class QuotationBase(BaseModel):
    quotation_id: Optional[int] = None
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None

    amount_including_gst: Optional[float] = 0
    without_gst: Optional[float] = 0
    gst_amount: Optional[float] = 0
    amount_with_gst: Optional[float] = 0

    additional_discount_percentage: int = 0
    additional_discount_amount: float = 0
    amount_after_discount: float = 0

    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None

    client_id: int
    created_at: Optional[datetime] = None
    created_by: Optional[str] = "System"


class QuotationCreate(BaseModel):
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None

    amount_including_gst: Optional[float] = 0
    without_gst: Optional[float] = 0
    gst_amount: Optional[float] = 0
    amount_with_gst: Optional[float] = 0

    additional_discount_percentage: Optional[int] = 0
    additional_discount_amount: Optional[float] = 0
    amount_after_discount: Optional[float] = 0

    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None

    client_id: int
    created_by: Optional[str] = "System"


class QuotationUpdate(QuotationCreate):
    pass


class Quotation(QuotationBase):
    model_config = ConfigDict(from_attributes=True)