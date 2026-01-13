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

    salesperson = Column(String(50), nullable=True)
    subject = Column(String(50), nullable=True)

    # 💰 Amounts (Decimal safe)
    amount_including_gst = Column(Numeric(12, 2), nullable=True)
    without_gst = Column(Numeric(12, 2), nullable=True)
    gst_amount = Column(Numeric(12, 2), nullable=True)
    amount_with_gst = Column(Numeric(12, 2), nullable=True)

    warranty_guarantee = Column(String(100), nullable=True)
    remarks = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)

    date = Column(Date, nullable=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(255), nullable=False, default="System")

    # 🔁 Relationships
    client = relationship("Client", back_populates="switches_quotation_wa")
    items = relationship(
        "SwitchQuotationItem_Wa",
        back_populates="switch_quotation_wa",
        cascade="all, delete-orphan"
    )
