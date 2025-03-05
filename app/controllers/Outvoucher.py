from sqlalchemy.orm import Session
from app.schema.outvoucher import Outvoucher, OutvoucherCreate, OutvoucherUpdate
from app.schema.outvoucher_item import OutvoucherItemCreate, OutvoucherItem
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_connection
# from app.controllers.Outvoucher import create_outvoucher, get_outvouchers, get_outvoucher_by_id, update_outvoucher

router = APIRouter()

@router.post("/outvouchers/", response_model=Outvoucher)
def create_voucher(outvoucher: OutvoucherCreate, db: Session = Depends(get_db_connection)):
    """Create a new outvoucher."""
    return create_outvoucher(db, outvoucher)

@router.get("/outvouchers/{voucher_id}", response_model=Outvoucher)
def read_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Retrieve a specific outvoucher by ID."""
    outvoucher = get_outvoucher_by_id(db, voucher_id)
    if not outvoucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return outvoucher

@router.get("/outvouchers/", response_model=List[Outvoucher])
def read_all_vouchers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    """Retrieve all outvouchers with pagination."""
    return get_outvouchers(db, skip, limit)

@router.put("/outvouchers/{voucher_id}", response_model=Outvoucher)
def update_voucher(voucher_id: int, outvoucher_update: OutvoucherUpdate, db: Session = Depends(get_db_connection)):
    """Update an existing outvoucher."""
    updated_voucher = update_outvoucher(db, voucher_id, outvoucher_update)
    if not updated_voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return updated_voucher

@router.delete("/outvouchers/{voucher_id}")
def delete_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Delete an outvoucher."""
    success = delete_outvoucher(db, voucher_id)
    if not success:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return {"message": "Voucher deleted successfully"}


def create_outvoucher(db: Session, outvoucher_data: OutvoucherCreate):
    new_outvoucher = Outvoucher(**outvoucher_data.model_dump())
    db.add(new_outvoucher)
    db.commit()
    db.refresh(new_outvoucher)
    return new_outvoucher

def create_outvoucher_item(db: Session, voucher_id: int, item: OutvoucherItemCreate):
    db_voucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not db_voucher:
        raise HTTPException(status_code=404, detail="Outvoucher not found")
    
    item_data = item.model_dump(exclude={"item_id", "voucher_id"})
    db_item = OutvoucherItem(voucher_id=db_voucher.id, **item_data)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_outvouchers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Outvoucher).offset(skip).limit(limit).all()

def get_outvoucher_by_id(db: Session, voucher_id: int):
    db_outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not db_outvoucher:
        raise HTTPException(status_code=404, detail="Outvoucher not found")
    return db_outvoucher

def get_outvoucher_items_by_voucher_id(db: Session, voucher_id: int) -> List[OutvoucherItem]:
    items = db.query(OutvoucherItem).filter(OutvoucherItem.voucher_id == voucher_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this voucher ID")
    return items

def update_outvoucher(db: Session, voucher_id: int, update_data: OutvoucherUpdate):
    db_outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not db_outvoucher:
        raise HTTPException(status_code=404, detail="Outvoucher not found")
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_outvoucher, key, value)
    db.commit()
    db.refresh(db_outvoucher)
    return db_outvoucher

def delete_outvoucher(db: Session, voucher_id: int):
    db_outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not db_outvoucher:
        raise HTTPException(status_code=404, detail="Outvoucher not found")
    db.delete(db_outvoucher)
    db.commit()
    return {"message": "Outvoucher deleted successfully"}
