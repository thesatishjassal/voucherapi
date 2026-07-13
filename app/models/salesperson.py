from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class SalesPerson(Base):
    __tablename__ = "salespersons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    architecture_name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)

    # ── team login OTP fields ──
    otp = Column(String(6), nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)