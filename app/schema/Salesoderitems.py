from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class SalesoderItemBase(BaseModel):
    """Base schema for Salesoderitems items aligned with the product info table."""
    salesoderitems_id: Optional[int] = Field(None, description="Associated Salesoderitems ID")
    product_id: Optional[str] = Field(None, description="Product unique identifier")
    customercode: Optional[str] = Field(None, description="Customer code")
    customerdescription: Optional[str] = Field(None, description="Customer product description")
    image: Optional[str] = Field(None, description="Image URL or path")
    itemcode: Optional[str] = Field(None, description="Item code")
    brand: Optional[str] = Field(None, description="Brand name")
    mrp: Optional[int] = Field(None, description="Maximum Retail Price")
    price: Optional[int] = Field(None, description="Price for Salesoderitems")
    quantity: int = Field(..., description="Quantity of product", ge=0)
    discount: int = Field(..., description="Discount percentage", ge=0)
    item_name: Optional[str] = Field(None, description="Name of the item")
    unit: Optional[str] = Field(None, description="Measurement unit (e.g., pcs, box)")

    model_config = ConfigDict(from_attributes=True)


class SalesoderItemCreate(SalesoderItemBase):
    """Schema for creating a new Salesoderitems item (without ID)."""
    pass  # No ID required as it's auto-generated


class SalesoderItemResponse(SalesoderItemBase):
    """Schema for responding with Salesoderitems item data including item_id mapped from 'id'."""
    item_id: int = Field(..., alias="id", description="Auto-generated unique identifier for the item")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)  # ✅ Support aliasing 'id' to 'item_id'
