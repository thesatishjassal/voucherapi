from pydantic import BaseModel, Field
from typing import Optional

class InvoucherItemBase(BaseModel):
    """Base schema for invoucher items."""
    invoucher_id: int
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
        orm_mode = True  # Enables compatibility with ORM objects

class InvoucherItemCreate(InvoucherItemBase):
    """Schema for creating a new invoucher item."""
    pass

class InvoucherItem(InvoucherItemBase):
    """Schema for responding with invoucher item data."""
    item_id: int

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects
