from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class SalesorderItems(Base):
    __tablename__ = "salesorderitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))
    customercode = Column(String(100), nullable=True)
    customerdescription = Column(String(100), nullable=True)  # ✅ Lowercase
    image = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)  # ✅ Lowercase
    brand = Column(String(100), nullable=True)
    mrp = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)

    # Relationships
    salesorders = relationship("SalesOrder", back_populates="items")
    product = relationship("Products", back_populates="salesorderitems")
