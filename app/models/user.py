from sqlalchemy import Column, Integer, String
from base import Base  # Import the shared Base from base.py

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String(15), unique=True, index=True)  # E.164 format max length 15
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone={self.phone}, password={self.password})>"

class Login(Base):
    __tablename__ = "login"
    __table_args__ = {"extend_existing": True}  # Optional, only if needed

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True)  # E.164 format max length 15
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone}, password={self.password})>"
