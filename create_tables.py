from app.models.user import Base  # Replace with the actual import path
from sqlalchemy import create_engine

# Replace 'postgresql://user:password@localhost/mydatabase' with your actual database URL
engine = create_engine('postgresql://postgres:123@localhost/postgres')

# Create all tables
Base.metadata.create_all(engine)
