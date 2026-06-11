from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base  # adjust import to your project


class ArchReference(Base):
    """
    A salesperson adds an architect they have met / are working with.
    One salesperson can reference many architects; one architect can be
    referenced by many salespersons.
    """
    __tablename__ = "arch_references"

    id              = Column(Integer, primary_key=True, index=True)

    # The salesperson who is adding the reference
    # sales_person_id = Column(Integer, ForeignKey("arch_registers.id", ondelete="CASCADE"), nullable=False)

    # The architect being referenced
    # architect_id    = Column(Integer, ForeignKey("arch_registers.id", ondelete="CASCADE"), nullable=False)
    sales_person_id = Column(Integer, ForeignKey("arch_register_users.id", ondelete="CASCADE"), nullable=False)
    architect_id    = Column(Integer, ForeignKey("arch_register_users.id", ondelete="CASCADE"), nullable=False)
    # Optional notes the salesperson can attach (e.g. "Met at expo 2025")
    notes           = Column(Text, nullable=True)

    added_at        = Column(DateTime, default=datetime.utcnow)

    # ── Relationships ────────────────────────────────────────
    sales_person = relationship(
        "ArchRegister",
        foreign_keys=[sales_person_id],
        back_populates="references_added"
    )

    architect = relationship(
        "ArchRegister",
        foreign_keys=[architect_id],
        back_populates="referenced_by"
    )