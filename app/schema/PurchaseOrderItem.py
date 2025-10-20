from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class PurchaseOrderItemBase(BaseModel):
    """Base schema for PurchaseorderItems aligned with the product info table."""
    purchaseorderitems_id: Optional[int] = Field(None, description="Associated PurchaseorderItems ID")
    product_id: Optional[str] = Field(None, description="Product unique identifier")
    customercode: Optional[str] = Field(None, description="Customer code")
    customerdescription: Optional[str] = Field(None, description="Customer product description")
    image: Optional[str] = Field(None, description="Image URL or path")
    itemcode: Optional[str] = Field(None, description="Item code")
    brand: Optional[str] = Field(None, description="Brand name")
    mrp: Optional[int] = Field(None, description="Maximum Retail Price")
    price: Optional[int] = Field(None, description="Price for PurchaseorderItem")
    quantity: int = Field(..., description="Quantity of product", ge=0)
    discount: int = Field(..., description="Discount percentage", ge=0)
    item_name: Optional[str] = Field(None, description="Name of the item")
    unit: Optional[str] = Field(None, description="Measurement unit (e.g., pcs, box)")
    color: Optional[str] = Field(None, description="color")
    remarks: Optional[str] = Field(None, description="remarks")

    model_config = ConfigDict(from_attributes=True)


class PurchaseorderItemCreate(PurchaseOrderItemBase):
    """Schema for creating a new PurchaseorderItem (without ID)."""
    pass


class PurchaseorderItemResponse(PurchaseOrderItemBase):
    """Schema for responding with PurchaseorderItem data including item_id mapped from 'id'."""
    item_id: int = Field(..., alias="id", description="Auto-generated unique identifier for the item")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
