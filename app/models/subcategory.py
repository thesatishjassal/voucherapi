from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py

class SubCategory(Base):
    __tablename__ = "subcategory"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed

    id = Column(Integer, primary_key=True, index=True)
    catname = Column(String)
    subcatname = Column(String)
    slug = Column(String)

    def __repr__(self):
        return f"<SubCategory (id={self.id}, Catname={self.catname}, Subcatname={self.subcatname}, Slug={self.subcatname}>"
