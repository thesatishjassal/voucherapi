from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # Import the shared Base
from models import User  # This ensures the User model is registered with Base

# Define the database URL
SQL_DB_URL = "postgresql://postgres:123@localhost/vocherdb"

# Create the engine
engine = create_engine(SQL_DB_URL)

# Create the tables in the database if they do not exist.
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

# Create a configured "SessionLocal" class.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency: Get a database session.
def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
