"""Pydantic schemas for Invoucher data validation in the IN Voucher API."""

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class InvoucherBase(BaseModel):
    id: Optional[int] = None
    voucher_id: Optional[int] = None
    voucher_number: str
    transaction_type: Optional[str] = "Transfer"
    voucher_date: date
    client_id: int
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    mode_of_transport: Optional[str] = None
    number_of_packages: Optional[int] = None
    freight_status: Optional[str] = "Paid"
    total_amount: Optional[float] = 0.00
    remarks: Optional[str] = None

class InvoucherCreate(InvoucherBase):
    """Schema for creating a new invoucher."""
    pass

class InvoucherUpdate(InvoucherBase):
    """Schema for updating an existing invoucher."""
    pass

class InvoucherItemSchema(BaseModel):
    pass


class Invoucher(InvoucherBase):
    """Schema for responding with invoucher data."""
    voucher_id: int

    model_config = ConfigDict(from_attributes=True)  # For ORM support
