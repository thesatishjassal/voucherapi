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
    price: float
    quantity: int
    rackcode: str
    size: str
    color: str
    model: str
    brand: str
    unit: str
    reorderqty: Optional[int] = None

    # ✅ New text fields
    cct: Optional[str] = None
    beamangle: Optional[str] = None
    cutoutdia: Optional[str] = None

    # ✅ Optional field
    in_display: Optional[bool] = True


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
    price: Optional[float] = None
    quantity: Optional[int] = None
    rackcode: Optional[str] = None
    thumbnail: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    reorderqty: Optional[int] = None

    # ✅ New text fields
    cct: Optional[str] = None
    beamangle: Optional[str] = None
    cutoutdia: Optional[str] = None

    # ✅ Optional field
    in_display: Optional[bool] = None


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
    price: Optional[float]
    quantity: int
    rackcode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str
    reorderqty: Optional[int] = None

    # ✅ New text fields
    cct: Optional[str] = None
    beamangle: Optional[str] = None
    cutoutdia: Optional[str] = None

    # ✅ Optional field
    in_display: Optional[bool] = None

    message: Optional[str] = None
    invoucher_items: Optional[List[dict]] = None

    model_config = ConfigDict(from_attributes=True)
