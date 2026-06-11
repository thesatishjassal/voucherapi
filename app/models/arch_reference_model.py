from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class ArchRegister(Base):

    __tablename__ = "arch_register_users"

    id = Column(Integer, primary_key=True, index=True)

    # AUTH

    role = Column(
        String,
        nullable=False,
        default="architect"
    )

    is_approved = Column(
        Boolean,
        default=False
    )

    # STEP 1

    full_name = Column(String, nullable=False)

    firm_name = Column(String, nullable=False)

    mobile_number = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=False
    )

    profession = Column(
        String,
        nullable=False
    )

    marital_status = Column(
        String,
        nullable=False
    )

    anniversary_date = Column(
        Date,
        nullable=True
    )

    # STEP 2

    account_holder_name = Column(
        String,
        nullable=False
    )

    bank_name = Column(
        String,
        nullable=False
    )

    account_number = Column(
        String,
        nullable=False
    )

    ifsc_code = Column(
        String,
        nullable=False
    )

    upi_id = Column(
        String,
        nullable=True
    )

    # PROFILE IMAGE

    profile_image = Column(
        String,
        nullable=True
    )

    # RELATIONSHIPS

    references_added = relationship(
        "ArchReference",
        foreign_keys="ArchReference.sales_person_id",
        back_populates="sales_person"
    )

    referenced_by = relationship(
        "ArchReference",
        foreign_keys="ArchReference.architect_id",
        back_populates="architect"
    )


class ArchReference(Base):
    """
    A salesperson adds an architect they have met / are working with.
    One salesperson can reference many architects; one architect can be
    referenced by many salespersons.
    """
    __tablename__ = "arch_references"

    id = Column(Integer, primary_key=True, index=True)

    sales_person_id = Column(
        Integer,
        ForeignKey("arch_register_users.id", ondelete="CASCADE"),
        nullable=False
    )

    architect_id = Column(
        Integer,
        ForeignKey("arch_register_users.id", ondelete="CASCADE"),
        nullable=False
    )

    notes = Column(Text, nullable=True)

    added_at = Column(DateTime, default=datetime.utcnow)

    # RELATIONSHIPS

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