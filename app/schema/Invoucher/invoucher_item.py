"""Pydantic schemas for InvoucherItem data validation in the IN Voucher API."""

from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import relationship

class InvoucherItemBase(BaseModel):
    """Base schema for invoucher items."""
    invoucher_id: int  # Fixed to match SQLAlchemy model
    product_id: Optional[int] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    rate: float
    discount_percentage: float = 0.00  # Removed Optional to avoid conflict
    amount: float
    comments: Optional[str] = None
    
    product = relationship("Products", back_populates="invoucher_items")

class InvoucherItemCreate(InvoucherItemBase):
    """Schema for creating a new invoucher item."""
    pass

class InvoucherItem(InvoucherItemBase):
    """Schema for responding with invoucher item data."""
    item_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 (use orm_mode=True in v1)
