from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class ProductsCreate(BaseModel):
    hsncode: str
    itemCode: str
    itemName: str
    description: str
    category: str
    subCategory: str
    price: str
    quantity: str
    rackCode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str

class ProductsUpdate(BaseModel):
    hsncode: Optional[str] = None
    itemCode: Optional[str] = None
    itemName: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subCategory: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    rackCode: Optional[str] = None
    thumbnail: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None

class ProductsResponse(BaseModel):
    id: int
    hsncode: str
    itemCode: str
    itemName: str
    description: str
    category: str
    subCategory: str
    price: str
    quantity: str
    rackCode: str
    thumbnail: Optional[str] = None
    size: str
    color: str
    model: str
    brand: str
    message: Optional[str] = None
    
model_config = ConfigDict(from_attributes=True)