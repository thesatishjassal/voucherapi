from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuotationItemHistorySchema(BaseModel):
    id: Optional[int]
    quotation_item_id: int
    quotation_id: Optional[int]
    product_id: Optional[str]
    customercode: Optional[str]
    customerdescription: Optional[str]
    image: Optional[str]
    itemcode: Optional[str]
    brand: Optional[str]
    mrp: Optional[int]
    price: Optional[int]
    quantity: Optional[int]
    discount: Optional[int]
    item_name: Optional[str]
    unit: Optional[str]
    edited_at: Optional[datetime]
    action: Optional[str]
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None


class QuotationItemHistoryResponse(BaseModel):
    id: int
    quotation_item_id: int
    quotation_id: int
    product_id: Optional[str]
    customercode: Optional[str]
    customerdescription: Optional[str]
    image: Optional[str]
    itemcode: Optional[str]
    brand: Optional[str]
    mrp: Optional[float]
    price: Optional[float]
    quantity: Optional[int]
    discount: Optional[float]
    item_name: Optional[str]
    unit: Optional[str]
    edited_at: datetime
    action: str
    amount_including_gst: Optional[int] = None
    without_gst: Optional[int] = None
    gst_amount: Optional[int] = None
    amount_with_gst: Optional[int] = None


    class Config:
        from_attributes = True
