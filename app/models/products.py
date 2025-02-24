from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__ = "products"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed

    id = Column(Integer, primary_key=True, index=True)
    hsncode = Column(String, name="hsncode", unique=True)  # Force lowercase column name
    itemCode = Column(String, name="itemcode",unique=True)
    itemName = Column(String, name="itemname",unique=True)
    description = Column(String, name="description")
    category = Column(String, name="category")
    subCategory = Column(String, name="subcategory")
    price = Column(String, name="price")
    quantity = Column(String, name="quantity")
    rackCode = Column(String, name="rackcode")
    thumbnail = Column(String, name="thumbnail", nullable=True)
    size = Column(String, name="size")
    color = Column(String, name="color")
    model = Column(String, name="model")
    brand = Column(String, name="brand")

    items = relationship("InvoucherItem", back_populates="products")

    def __repr__(self):
        return f"<Products (id={self.id}, hsncode={self.hsncode},itemCode={self.itemCode},itemName={self.itemName},description={self.description},category={self.category}, subCategory={self.subCategory},price={self.price}, quantity={self.quantity},rackCode={self.rackCode}, thumbnail={self.thumbnail}, size={self.size},color={self.color},model={self.model},brand={self.brand})>"