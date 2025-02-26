from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base  # Use centralized Base

class Products(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True)
    itemcode = Column(String, unique=True)
    item_name = Column(String)
    description = Column(String)
    category = Column(String)
    sub_category = Column(String)
    price = Column(String)
    quantity = Column(String)
    rack_code = Column(String)
    thumbnail = Column(String, nullable=True)
    size = Column(String)
    color = Column(String)
    model = Column(String)
    brand = Column(String)

    items = relationship("InvoucherItem", back_populates="product")  # ✅ Remove `and`
