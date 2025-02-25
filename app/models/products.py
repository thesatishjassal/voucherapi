# product.py
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.orm import declarative_base

# Create a single Base instance for the entire project.
Base = declarative_base()

class Products(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, unique=True)
    item_code = Column(String, unique=True)
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

    # items = relationship("InvoucherItem", back_populates="products")    
    invoucher_item_id = Column(Integer, ForeignKey("invoucher_item.id"))
    invoucher_item = relationship("InvoucherItem", back_populates="products")

    @declared_attr
    def invoucher_item(cls):
        return relationship("InvoucherItem", back_populates="products")