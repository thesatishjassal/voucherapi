from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal


class QuotationBase(BaseModel):
    quotation_id: Optional[int] = None
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None

    # ✅ ADD ONLY (no changes)
    gst_type: Optional[Literal["include", "exclude"]] = "include"
    gst_percentage: Optional[float] = 0

    additional_discount_percentage: int = 0
    additional_discount_amount: float = 0
    amount_after_discount: float = 0

    # ✅ OPTIONAL BUT VERY USEFUL (ADD)
    final_amount: Optional[float] = None

    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None
    client_id: int
    created_at: Optional[datetime] = None
    created_by: str

class QuotationCreate(BaseModel):
    quotation_no: str
    salesperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None

    # ✅ ADD HERE ALSO
    gst_type: Optional[Literal["include", "exclude"]] = "include"
    gst_percentage: Optional[float] = 0

    additional_discount_percentage: Optional[int] = 0
    additional_discount_amount: Optional[int] = 0
    amount_after_discount: Optional[int] = None

    # ✅ ADD
    final_amount: Optional[float] = None

    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None
    client_id: int
    created_by: Optional[str] = None
    
class QuotationUpdate(QuotationBase):
    pass

class Quotation(QuotationBase):
    model_config = ConfigDict(from_attributes=True)