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

    # 📌 SR No
    sr_no = Column(Integer, nullable=True, index=True)

    # 🧾 Item Details
    item_name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    color = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    itemcode = Column(String(100), nullable=True)
    image = Column(String(150), nullable=True)

    # 📦 Pricing
    quantity = Column(Integer, nullable=False)
    mrp = Column(Numeric(10, 2), nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)

    # 💸 Discount
    discount_percent = Column(Numeric(5, 2), nullable=False)
    net_price = Column(Numeric(12, 2), nullable=True)

    # 📝 Misc
    unit = Column(String(20), nullable=True)
    remarks = Column(String(500), nullable=True)

    # 🔁 Relationship
    switch_quotation = relationship(
        "SwitchQuotation_Wa",
        back_populates="items"
    )
