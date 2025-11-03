from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base model for shared fields
class PurchaseOrderBase(BaseModel):
    purchaseorder_id: Optional[int] = None
    purchaseorder_no: str
    purchaseperson: Optional[str] = None
    subject: Optional[str] = None
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None
    remarks: Optional[str] = None
    status: Optional[str] = None
    date: Optional[datetime] = None
    client_id: int  # Required
    created_by: Optional[str] = None
    
    payment_method: Optional[str] = None
    freight: Optional[str] = None
    issue_slip_no: Optional[str] = None

    class Config:
        from_attributes = True  # ORM compatibility

# ✅ Correct names for import
class PurchaseOrderCreate(PurchaseOrderBase):
    pass  # For creating new purchase orders

class PurchaseOrderUpdate(PurchaseOrderBase):
    pass  # For updating existing purchase orders

class PurchaseOrder(PurchaseOrderBase):
    model_config = ConfigDict(from_attributes=True)
    purchaseorder_id: int
