from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timedelta


class ArchOtp(Base):
    __tablename__ = "arch_otps"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), index=True, nullable=False)

    otp_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    expires_at = Column(
        DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=5)
    )