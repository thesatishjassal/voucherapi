# schemas/invoucher.py
"""Pydantic schemas for Invoucher data validation in the IN Voucher API."""

from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoucherBase(BaseModel):
    """Base schema for invouchers."""
    voucher_number: str
    transaction_type: Optional[str] = "Transfer"
    voucher_date: date
    client_id: int
    invoice_number: Optional[str] = None  # Receiver detail: Invoice Number
    invoice_date: Optional[date] = None  # Receiver detail: Invoice Date
    mode_of_transport: Optional[str] = None  # Receiver detail: Mode of Transport
    number_of_packages: Optional[int] = None  # Receiver detail: Number of Packages
    freight_status: Optional[str] = "Paid"
    total_amount: Optional[float] = 0.00
    remarks: Optional[str] = None

class InvoucherCreate(InvoucherBase):
    """Schema for creating a new invoucher."""
    pass

class InvoucherUpdate(InvoucherBase):
    """Schema for updating an existing invoucher."""
    pass

class Invoucher(InvoucherBase):
    """Schema for responding with invoucher data."""
    voucher_id: int

    class Config:
        orm_mode = True