from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import User, Base  # Import your model

SQL_DB_URL = "postgresql://postgres:123@localhost/vocherdb"

engine = create_engine(SQL_DB_URL)

# Create the tables if they do not exist
# Base = declarative_base()
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
