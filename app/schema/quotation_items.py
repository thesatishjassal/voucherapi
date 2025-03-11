from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class QuotationItemBase(BaseModel):
    """Base schema for Quotation items aligned with the product info table."""
    quotation_id: Optional[int] = None
    product_id: Optional[str] = None
    customercode: Optional[str] = None
    customerdescription: Optional[str] = None
    image: Optional[str] = None
    itemcode: Optional[str] = None
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
    # No item_id or id here (handled by DB)
    pass

class QuotationItemResponse(QuotationItemBase):
    """Schema for responding with Quotation item data including item_id mapped from 'id'."""
    item_id: int = Field(..., description="Auto-generated unique identifier for the item")  # ✅ Expose `id` as `item_id`

    model_config = ConfigDict(from_attributes=True)
