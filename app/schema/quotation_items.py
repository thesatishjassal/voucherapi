from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class QuotationItemBase(BaseModel):
    """Base schema for Quotation items aligned with the product info table."""

    quotation_id: Optional[int] = Field(None, description="Associated quotation ID")
    product_id: Optional[str] = Field(None, description="Product unique identifier")
    customercode: Optional[str] = Field(None, description="Customer code")
    customerdescription: Optional[str] = Field(
        None,
        description="Customer product description"
    )
    image: Optional[str] = Field(None, description="Image URL or path")
    itemcode: Optional[str] = Field(None, description="Item code")
    brand: Optional[str] = Field(None, description="Brand name")

    # ✅ Money fields as float to allow decimals
    mrp: Optional[float] = Field(None, description="Maximum Retail Price")
    netPrice: Optional[float] = Field(None, description="Net price for quotation")
    price: Optional[float] = Field(None, description="Price for quotation")

    quantity: int = Field(..., description="Quantity of product", ge=0)
    discount: int = Field(..., description="Discount percentage", ge=0)
    item_name: Optional[str] = Field(None, description="Name of the item", max_length=100)
    unit: Optional[str] = Field(None, description="Measurement unit (e.g., pcs, box)")

    # ✅ All amount fields as float for fractional values
    amount_including_gst: Optional[float] = None
    without_gst: Optional[float] = None
    gst_amount: Optional[float] = None
    amount_with_gst: Optional[float] = None
    amount: Optional[float] = None

    # Extra optional descriptive fields
    cct: Optional[str] = Field(None, description="Correlated Color Temperature (e.g., 3000K, 4000K)")
    beamangle: Optional[str] = Field(None, description="Beam angle of the light (in degrees)")
    cri: Optional[str] = Field(None, description="Color Rendering Index (e.g., >80, >90)")
    cutoutdia: Optional[str] = Field(None, description="Cutout diameter size")
    lumens: Optional[str] = Field(None, description="Luminous flux (brightness)")

    model_config = ConfigDict(from_attributes=True)


class QuotationItemCreate(QuotationItemBase):
    """Schema for creating a new Quotation item (without ID)."""
    pass  # ID auto-generated


class QuotationItemResponse(QuotationItemBase):
    """Schema for responding with Quotation item data including item_id mapped from 'id'."""
    item_id: int = Field(..., alias="id", description="Auto-generated unique identifier for the item")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
