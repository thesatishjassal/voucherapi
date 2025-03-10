"""Pydantic schemas for Quotation data validation in the IN Voucher API."""

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

from sqlalchemy import Boolean

class QuotationBase(BaseModel):
    id: Optional[int] = None
    quotation_id: int
    quotation_number: str
    salesperson: Optional[str] = None
    subject:  Optional[date] = None
    amount_including_GST: Optional[int] = None
    without_GST: Optional[int] = None
    GST_ammount: Optional[int] = None
    amount_withGST: Optional[int] = None
    warranty_guarantee: Optional[str] = None
    remarks: Optional[str] = None
    status: Optional[bool] = None
    date: Optional[date] = None
    client_id: int

class QuotationCreate(QuotationBase):
    """Schema for creating a new Quotation."""
    pass

class QuotationUpdate(QuotationBase):
    """Schema for updating an existing Quotation."""
    pass

class Quotation(QuotationBase):
    """Schema for responding with Quotation data."""
    quotation_id: int

    model_config = ConfigDict(from_attributes=True)  # For ORM support
