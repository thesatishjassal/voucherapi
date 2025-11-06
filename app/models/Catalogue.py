from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean
from database import Base

class Catalogue(Base):
    __tablename__ = "catalogues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    google_drive_url = Column(Text)  # Changed from pdf_url to store Google Drive link
    created_by = Column(String(100), nullable=False)  # New field for creator (e.g., user ID or name)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())