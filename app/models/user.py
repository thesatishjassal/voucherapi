from sqlalchemy import Column, Integer, String
from database import Base  # Use the shared Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # Allow redefinition if already defined

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String(15), unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone={self.phone}, password={self.password})>"
