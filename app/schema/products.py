from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# -----------------------------------------------
# ✅ Create Product Schema
# -----------------------------------------------
class ProductsCreate(BaseModel):
    hsncode: str
    itemcode: str
    itemname: str
    description: str
    category: str
    subcategory: str
    price: float  # Keeping price as float for arithmetic operations
    quantity: int  # Quantity as integer for stock management
    rackcode: str
    size: str
    color: str
    model: str
    brand: str
    unit: str


# -----------------------------------------------
# ✅ Update Product Schema (Optional fields)
# -----------------------------------------------
class ProductsUpdate(BaseModel):
    hsncode: Optional[str] = None
    itemcode: Optional[str] = None
    itemname: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[float] = None  # Float for consistency
    quantity: Optional[int] = None  # Int for stock update
    rackcode: Optional[str] = None
    thumbnail: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None


# -----------------------------------------------
# ✅ Response Schema
# -----------------------------------------------
class ProductsResponse(BaseModel):
    id: int
    hsncode: str
    itemcode: str
    itemname: str
    description: str
    unit: str
    category: str
    subcategory: str
    price: float  # Return as float for frontend calculations
    quantity: int  # Return as int
    rackcode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str
    message: Optional[str] = None
    invoucher_items: Optional[List[dict]] = None  # If relational, replace dict with specific schema later

    model_config = ConfigDict(from_attributes=True)
