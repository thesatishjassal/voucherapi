from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)  # Ensures email is unique

# Additional models can be added below

# In case you want to create the tables in the database directly using SQLAlchemy
# from database import engine
# Base.metadata.create_all(bind=engine)
