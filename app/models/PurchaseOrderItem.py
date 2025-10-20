from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class PurchaseOrderItems(Base):
    __tablename__ = "purchaseorderitems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    purchaseorder_id = Column(Integer, ForeignKey("purchaseorders.purchaseorder_id"), nullable=True)
    product_id = Column(String(50), ForeignKey("products.itemcode"))

    customercode = Column(String(100), nullable=True)
    customerdescription = Column(String(100), nullable=True)
    image = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    mrp = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    item_name = Column(String(100), nullable=True)
    unit = Column(String(20), nullable=True)
    color = Column(String(20), nullable=True)
    remarks = Column(String(20), nullable=True)

    # Relationships
    purchaseorder = relationship("SalesOrder", back_populates="purchaseitems")
    product = relationship("Products", back_populates="purchaseitems")