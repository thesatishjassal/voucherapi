from pydantic import BaseModel
from typing import Optional

class InvoucherItemBase(BaseModel):
    """Base schema for invoucher items."""
    voucher_id: int
    product_id: Optional[int] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    rate: float
    discount_percentage: float = 0.00
    amount: float
    comments: Optional[str] = None

    class Config:
        from_attributes = True  # Enables compatibility with ORM objects

class InvoucherItemCreate(InvoucherItemBase):
    """Schema for creating a new invoucher item."""
    product_id: Optional[int] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    rate: float
    discount_percentage: float = 0.00
    amount: float
    comments: Optional[str] = None

class InvoucherItem(InvoucherItemBase):
    """Schema for responding with invoucher item data."""
    item_id: int

    class Config:
        from_attributes = True  # Enables compatibility with ORM objects

class InvoucherItemResponse(InvoucherItemCreate):
    item_id: int  # ✅ Include item_id in response but not in create
