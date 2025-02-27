from sqlalchemy.orm import Session
from app.models.invoucher import Invoucher
from app.schema.invoucher import Invoucher, InvoucherCreate, InvoucherUpdate
from app.schema.invoucher_item import InvoucherItem, InvoucherItemCreate
from fastapi import HTTPException  # If using FastAPI
from app.models.invoucher import Invoucher  # ✅ Ensure this is the correct import

# Invoucher CRUD Operations

def create_invoucher(db: Session, invoucher: InvoucherCreate):
    """Create a new invoucher."""
    db_invoucher = Invoucher(**invoucher.model_dump())  # Use SQLAlchemy model
    db.add(db_invoucher)
    db.commit()
    db.refresh(db_invoucher)
    return db_invoucher

def create_invoucher_item(db: Session, voucher_id: int, item: InvoucherItemCreate):
    """Create a new item for an invoucher."""
    db_voucher = db.query(Invoucher).filter(Invoucher.voucher_id == voucher_id).first()  # ✅ Correct query
    if not db_voucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    
    db_item = InvoucherItem(voucher_id=voucher_id, **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_invouchers(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve a list of invouchers."""
    return db.query(Invoucher).offset(skip).limit(limit).all()

def get_invoucher(db: Session, voucher_id: int):
    """Retrieve a specific invoucher by ID."""
    db_invoucher = db.query(Invoucher).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    return db_invoucher

def update_invoucher(db: Session, voucher_id: int, invoucher: InvoucherUpdate):
    """Update an existing invoucher."""
    db_invoucher = db.query(Invoucher).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")

    for key, value in invoucher.model_dump(exclude_unset=True).items():
        setattr(db_invoucher, key, value)

    db.commit()
    db.refresh(db_invoucher)
    return db_invoucher

def delete_invoucher(db: Session, voucher_id: int):
    """Delete an invoucher."""
    db_invoucher = db.query(Invoucher).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")

    db.delete(db_invoucher)
    db.commit()
    return {"message": "Invoucher deleted successfully"}
