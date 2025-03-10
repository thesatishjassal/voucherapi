from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class QuotationItemBase(BaseModel):
    """Base schema for Quotation items aligned with the product info table."""
    item_id: Optional[int] = None
    quotation_id: Optional[int] = None
    product_id: Optional[str] = None
    customercode: Optional[str] = None
    customerDescription: Optional[str] = None
    image: Optional[str] = None
    itemCode: Optional[str] = None
    brand: Optional[str] = None
    mrp: Optional[int] = None
    price: Optional[int] = None
    quantity: int
    discount: int
    item_name: Optional[str] = None
    unit: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class QuotationItemCreate(QuotationItemBase):
    """Schema for creating a new Quotation item."""
    item_id: Optional[int] = Field(None, description="Auto-generated ID, not required for creation")

class QuotationItem(QuotationItemBase):
    """Schema for representing an existing Quotation item."""
    item_id: int = Field(..., description="Unique identifier for the item")

    model_config = ConfigDict(from_attributes=True)

class QuotationItemResponse(QuotationItem):
    """Schema for responding with Quotation item data."""
    item_id: int  # ✅ Include item_id in response but not in creation
