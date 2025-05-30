from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.clients import Client
from base import Base  # Ensure base.py has Base = declarative_base()

SQL_DB_URL = "postgresql://postgres:123@localhost/vocherdb"

print("🔄 Connecting to Database...")
engine = create_engine(SQL_DB_URL)

print("📦 Creating Tables (if not exist)...")
# Base.metadata.drop_all(bind=engine)  # Delete all tables
Base.metadata.create_all(bind=engine)  # Recreate tables
print("✅ Tables Created Successfully!")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection(): 
    """Provide a transactional scope around a series of operations."""
    print("🔌 Opening Database Connection...")
    db = SessionLocal()
    try:
        yield db
        print("✅ Transaction Completed Successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()  # Rollback transaction in case of error
        raise e  # Ensure exception is re-raised to propagate it properly
    finally:
        db.close()
        print("🔒 Database Connection Closed.")
