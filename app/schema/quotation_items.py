from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class QuotationItemBase(BaseModel):
    """Base schema for Quotation items aligned with the product info table."""
    quotation_id: Optional[int] = Field(None, description="Associated quotation ID")
    product_id: Optional[str] = Field(None, description="Product unique identifier")
    customercode: Optional[str] = Field(None, description="Customer code")
    customerdescription: Optional[str] = Field(None, description="Customer product description")
    image: Optional[str] = Field(None, description="Image URL or path")
    itemcode: Optional[str] = Field(None, description="Item code")
    brand: Optional[str] = Field(None, description="Brand name")
    mrp: Optional[int] = Field(None, description="Maximum Retail Price")
    netPrice: Optional[int] = Field(None, description="NetPrice for quotation")
    price: Optional[int] = Field(None, description="Price for quotation")
    quantity: int = Field(..., description="Quantity of product", ge=0)
    discount: int = Field(..., description="Discount percentage", ge=0)
    item_name: Optional[str] = Field(None, description="Name of the item", max_length=100)
    unit: Optional[str] = Field(None, description="Measurement unit (e.g., pcs, box)")
    amount: int = Field(..., description="Total amount (quantity * netPrice)", ge=0)  # Added amount field
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None
    remarks: Optional[str] = Field(None, description="Additional remarks for the item", max_length=500)

    model_config = ConfigDict(from_attributes=True)

class QuotationItemCreate(QuotationItemBase):
    """Schema for creating a new Quotation item (without ID)."""
    pass  # No ID required as it's auto-generated

class QuotationItemResponse(QuotationItemBase):
    """Schema for responding with Quotation item data including item_id mapped from 'id'."""
    item_id: int = Field(..., alias="id", description="Auto-generated unique identifier for the item")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)  # Support aliasing 'id' to 'item_id'