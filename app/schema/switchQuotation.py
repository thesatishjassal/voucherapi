# schemas/switch_quotation.py
from pydantic import BaseModel

class SwitchQuotationBase(BaseModel):
    itemcode: str
    itemname: str
    module_size: str
    white_price: float
    silver_price: float
    glaxyblack_price: float
    inner_outlet_caselot: int
    category: str
    brand: str

class SwitchQuotationCreate(SwitchQuotationBase):
    pass

class SwitchQuotationSchema(SwitchQuotationBase):  # Renamed to avoid conflict
    id: int

    class Config:
        from_attributes = True
