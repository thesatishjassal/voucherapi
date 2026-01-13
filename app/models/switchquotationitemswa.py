from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from database import Base


class SwitchQuotationItem_Wa(Base):
    __tablename__ = "switch_quotation_items_wa"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    quotation_id = Column(
        Integer,
        ForeignKey("switches_quotation_wa.quotation_id", ondelete="CASCADE"),
        nullable=False
    )

    sr_no = Column(Integer, index=True)

    item_name = Column(Text)
    description = Column(Text)
    color = Column(String(50))
    category = Column(String(100))
    brand = Column(String(100))
    itemcode = Column(String(100))
    image = Column(String(150))

    quantity = Column(Integer, nullable=False)
    mrp = Column(Numeric(10, 2))
    amount = Column(Numeric(12, 2))

    discount_percent = Column(Numeric(5, 2), nullable=False)
    net_price = Column(Numeric(12, 2))

    unit = Column(String(20))
    remarks = Column(String(500))

    # ✅ FIXED relationship
    switch_quotation = relationship(
        "SwitchQuotation_Wa",
        back_populates="items"
    )
