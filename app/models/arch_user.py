from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class ArchUser(Base):
    __tablename__ = "arch_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)