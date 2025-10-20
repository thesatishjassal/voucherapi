from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base model with shared fields
class PurchaseOrderItemBase(BaseModel):
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
    color: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

# ✅ Models used in API
class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemUpdate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
