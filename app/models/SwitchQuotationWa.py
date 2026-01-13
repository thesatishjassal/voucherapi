from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Date,
    ForeignKey,
    Numeric,
    func
)
from sqlalchemy.orm import relationship
from database import Base


class SwitchQuotation_Wa(Base):
    __tablename__ = "switches_quotation_wa"

    quotation_id = Column(Integer, primary_key=True, index=True)
    quotation_no = Column(String(50), unique=True, nullable=False)

    salesperson = Column(String(50))
    subject = Column(String(50))

    amount_including_gst = Column(Numeric(12, 2))
    without_gst = Column(Numeric(12, 2))
    gst_amount = Column(Numeric(12, 2))
    amount_with_gst = Column(Numeric(12, 2))

    warranty_guarantee = Column(String(100))
    remarks = Column(String(255))
    status = Column(String(50))

    date = Column(Date)

    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=False, default="System")

    # ✅ FIXED relationships
    client = relationship(
        "Client",
        back_populates="switches_quotation_wa"
    )

    items = relationship(
        "SwitchQuotationItem_Wa",
        back_populates="switch_quotation",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
