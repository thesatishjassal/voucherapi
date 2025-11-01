"""Pydantic schemas for Outvoucher data validation in the IN Voucher API."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class OutvoucherBase(BaseModel):
    """Base schema for Outvoucher data."""
    id: Optional[int] = None
    voucher_id: Optional[int] = None  # Already optional here
    voucher_no: str = Field(..., description="Voucher No (e.g., #LL9378)")
    issue_slip_no: Optional[str] = Field(None, description="Issue Slip No (e.g., SLIP98765)")
    sale_order_no: Optional[str] = Field(None, description="Sale Order No (e.g., SO123456)")
    transport: Optional[str] = Field(None, description="Transport method (e.g., DHL)")
    vehicle_no: Optional[str] = Field(None, description="Vehicle No (e.g., PB 08: 1014)")
    number_of_packages: Optional[int] = Field(None, ge=0, description="Number of packages (e.g., 2)")
    ordered_by: Optional[str] = Field(None, description="Person who ordered (e.g., Johny)")
    sales_person: Optional[str] = Field(None, description="Sales person (e.g., John)")
    freight_amount: Optional[float] = Field(0.00, ge=0.0, description="Freight Amount (e.g., 200)")
    remarks: Optional[str] = Field(None, description="Remarks/Notes (optional)")
    receiver_name: Optional[str] = Field(None, description="Receiver Name")
    mobile_number: Optional[str] = Field(None, description="Mobile Number of receiver")
    client_id: Optional[int] = Field(None, description="Client Id is required")
    transaction_types: Optional[str] = Field(None, description="transaction_type")
    created_by: Optional[str] = "System"
    
class OutvoucherCreate(OutvoucherBase):
    """Schema for creating a new Outvoucher."""
    pass

class OutvoucherUpdate(OutvoucherBase):
    """Schema for updating an existing Outvoucher."""
    pass

class Outvoucher(OutvoucherBase):
    """Schema for responding with Outvoucher data."""
    voucher_id: Optional[int] = None  # Changed to Optional to allow None

    model_config = ConfigDict(from_attributes=True)  # For ORM support