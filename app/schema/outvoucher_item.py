from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class OutvoucherItemBase(BaseModel):
    """Base schema for Outvoucher items aligned with product info table."""
    voucher_id: Optional[int] = Field(None, description="Voucher identifier")
    product_id: Optional[str] = Field(None, description="Item Code from product info")
    item_name: Optional[str] = Field(None, description="Item Name from product info")
    unit: Optional[str] = Field(None, description="Unit from product info")
    rack_code: Optional[str] = Field(None, description="Rackcode from product info")
    quantity: int = Field(..., ge=0, description="Quantity of the product")  # ✅ Required and non-negative
    comments: Optional[str] = Field(None, description="Comments from product info")

    model_config = ConfigDict(
        from_attributes = True 
    )
    
class OutvoucherItemCreate(OutvoucherItemBase):
    """Schema for creating a new Outvoucher item."""
    item_id: Optional[int] = Field(None, description="Auto-generated ID, not required for creation")

class OutvoucherItem(OutvoucherItemBase):
    """Schema for representing an existing Outvoucher item."""
    item_id: int = Field(..., description="Unique identifier for the item")

    model_config = ConfigDict(
        from_attributes = True 
    )
class OutvoucherItemResponse(OutvoucherItem):
    """Schema for responding with Outvoucher item data."""
    item_id: int  # ✅ Include item_id in response but not in creation
