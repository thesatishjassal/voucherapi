from sqlalchemy import Column, Integer, String, Text
from database import Base

class BrandQR(Base):
    __tablename__ = "brand_qr_links"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String, unique=True)
    pdf_link = Column(Text)
    qr_code = Column(Text)