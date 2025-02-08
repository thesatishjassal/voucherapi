from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py

class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String)

    def __repr__(self):
        return f"<Category (id={self.id}, Name={self.name}, Slug={self.slug}>"
