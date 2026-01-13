from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class SwitchQuotationItemBase(BaseModel):
    sr_no: Optional[int] = None

    item_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    itemcode: Optional[str] = None
    image: Optional[str] = None

    quantity: int
    mrp: Optional[Decimal] = None
    amount: Optional[Decimal] = None

    discount_percent: Decimal
    net_price: Optional[Decimal] = None

    unit: Optional[str] = None
    remarks: Optional[str] = None


class SwitchQuotationItemCreate(SwitchQuotationItemBase):
    pass


class SwitchQuotationItemSchema(SwitchQuotationItemBase):
    id: int
    quotation_id: int

    class Config:
        from_attributes = True
