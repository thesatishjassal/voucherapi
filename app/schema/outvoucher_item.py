from pydantic import BaseModel
from typing import Optional

class OutvoucherItemBase(BaseModel):
    sr_no: Optional[int] = None
    product_id: Optional[str] = None
    item_name: Optional[str] = None
    unit: Optional[str] = None
    rack_code: Optional[str] = None
    quantity: int
    comments: Optional[str] = None

class OutvoucherItemCreate(OutvoucherItemBase):
    pass

class OutvoucherItem(OutvoucherItemBase):
    item_id: int
    voucher_id: int

    class Config:
        orm_mode = True
