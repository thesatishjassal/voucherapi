from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # Import the shared Base

SQL_DB_URL = "postgresql://postgres:123@localhost/vocherdb"

# Create the engine
engine = create_engine(SQL_DB_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
