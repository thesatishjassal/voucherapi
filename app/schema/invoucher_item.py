from pydantic import BaseModel
from typing import Optional

class InvoucherItemBase(BaseModel):
    """Base schema for invoucher items."""
    product_id: int
    item_name: str
    unit: str
    rack_code: str
    quantity: int
    rate: float
    discount_percentage: float = 0.00
    amount: float
    comments: Optional[str] = None

    class Config:
        from_attributes = True  # Enables compatibility with ORM objects

class InvoucherItemCreate(InvoucherItemBase):
    """Schema for creating a new invoucher item."""
    pass

class InvoucherItem(InvoucherItemBase):
    """Schema for responding with invoucher item data."""
    item_id: int
    voucher_id: int  # ✅ Added to response but NOT in Create schema

    class Config:
        from_attributes = True
