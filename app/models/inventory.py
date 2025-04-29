from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from base import Base
import enum

# Inventory action types
class ActionType(str, enum.Enum):
    RETURN = "return"
    BOOK = "book"
    HOLD = "hold"

# Log every inventory transaction
class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True)
    itemcode = Column(String, ForeignKey("products.itemcode"))
    action_type = Column(Enum(ActionType), nullable=False)
    quantity = Column(Integer, nullable=False)
    action_date = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Products", backref="inventory_logs")

# Store items that are on hold
class HoldItem(Base):
    __tablename__ = "holds"

    id = Column(Integer, primary_key=True)
    itemcode = Column(String, ForeignKey("products.itemcode"))
    quantity = Column(Integer, nullable=False)
    hold_reason = Column(String, nullable=True)
    hold_date = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Products", backref="held_items")
