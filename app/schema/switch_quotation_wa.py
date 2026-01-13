from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime

from .switch_quotation_item_wa import SwitchQuotationItemCreate, SwitchQuotationItemSchema


class SwitchQuotationBase(BaseModel):
    quotation_no: str

    salesperson: Optional[str] = None
    subject: Optional[str] = None

    amount_including_gst: Optional[Decimal] = None
    without_gst: Optional[Decimal] = None
    gst_amount: Optional[Decimal] = None
    amount_with_gst: Optional[Decimal] = None

    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[str] = None

    date: Optional[date] = None # type: ignore
    client_id: int


class SwitchQuotationCreate(SwitchQuotationBase):
    items: List["SwitchQuotationItemCreate"]


class SwitchQuotationSchema(SwitchQuotationBase):
    quotation_id: int
    created_at: datetime
    created_by: str

    items: List[SwitchQuotationItemSchema] = []

    class Config:
        from_attributes = True
