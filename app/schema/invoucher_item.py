from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class InvoucherItemBase(BaseModel):
    """Base schema for invoucher items."""
    voucher_id: Optional[int] = None
    product_id: Optional[str] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    rate: float
    discount_percentage: float = 0.00
    additional_discount_percentage: float = 0.00  # Added new field
    amount: float
    comments: Optional[str] = None

    model_config = ConfigDict(
        from_attributes = True 
    )
    
class InvoucherItemCreate(InvoucherItemBase):
    """Schema for creating a new invoucher item."""
    item_id: Optional[int] = Field(None, description="Auto-generated ID")
    product_id: Optional[str] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    rate: float
    discount_percentage: float = 0.00
    additional_discount_percentage: float = 0.00  # Added new field
    amount: float
    comments: Optional[str] = None

class InvoucherItem(InvoucherItemBase):
    """Schema for responding with invoucher item data."""
    item_id: int

    model_config = ConfigDict(
        from_attributes = True 
    )
class InvoucherItemResponse(InvoucherItemCreate):
    item_id: int  # ✅ Include item_id in response but not in create