from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from database import Base

class Catalogue(Base):
    __tablename__ = "catalogues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    pdf_url = Column(Text)
    is_deleted = Column(Boolean, default=False)  # Optional: for soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())