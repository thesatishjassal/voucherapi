from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import declarative_base
from database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String(15), unique=True, index=True)  # Max length 15, E.164 format
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, phone={self.phone} , password={self.password})>"
    