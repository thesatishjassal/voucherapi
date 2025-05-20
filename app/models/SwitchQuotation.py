# models/switch_quotation.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

class SwitchQuotation(Base):
    __tablename__ = "switches_quotation"

    id = Column(Integer, primary_key=True, index=True)
    itemcode = Column(String, unique=True, index=True)
    itemname = Column(String)
    module_size = Column(String)
    white_price = Column(Float)
    silver_price = Column(Float)
    glaxyblack_price = Column(Float)
    inner_outlet_caselot = Column(Integer)
    category = Column(String)
    brand = Column(String)
