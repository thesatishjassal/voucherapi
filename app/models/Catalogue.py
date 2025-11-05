# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class Catalogue(Base):
    __tablename__ = "catalogues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    pdf_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
