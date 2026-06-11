from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean
)

from database import Base


class ArchRegister(Base):

    __tablename__ = "arch_register_users"
    __table_args__ = {"extend_existing": True}  # ✅ add this
    
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
