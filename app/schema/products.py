from typing import Optional, List
from pydantic import BaseModel

class ProductsCreate(BaseModel):
    hsncode: str
    itemcode: str
    itemname: str
    description: str
    category: str
    subcategory: str
    price: str
    quantity: str
    rackcode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str

class ProductsUpdate(BaseModel):
    hsncode: Optional[str] = None
    itemcode: Optional[str] = None
    itemname: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    rackcode: Optional[str] = None
    thumbnail: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None

class ProductsResponse(BaseModel):
    id: str
    hsncode: str
    itemcode: str
    itemname: str
    description: str
    category: str
    subcategory: str
    price: str
    quantity: str
    rackcode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str
    message: Optional[str] = None
    invoucher_items: Optional[List[dict]] = None  # Change this to List[InvoucherItemResponse] if you have a response schema

    class Config:
        from_attributes = True
