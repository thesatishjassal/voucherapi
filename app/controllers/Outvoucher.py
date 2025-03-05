from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.outvoucher import Outvoucher
from app.models.outvoucher_item import OutvoucherItem
from app.schema.outvoucher import Outvoucher, OutvoucherCreate
from app.schema.outvoucher_item import OutvoucherItem, OutvoucherItemCreate

def create_outvoucher(db: Session, outvoucher_data: OutvoucherCreate):
    new_outvoucher = Outvoucher(**outvoucher_data.dict())
    db.add(new_outvoucher)
    db.commit()
    db.refresh(new_outvoucher)
    return new_outvoucher

def create_outvoucher_item(db: Session, voucher_id: str, item: OutvoucherItemCreate):
    """Create a new item for an invoucher using invouchers.id."""
    db_voucher = db.query(OutvoucherItem).filter(OutvoucherItem.id == int(voucher_id)).first()
    if not db_voucher:
        raise HTTPException(status_code=404, detail="Outvoucher not found")
    
    item_data = item.model_dump(exclude={"item_id", "voucher_id"})
    # Use db_voucher.id (e.g., 48) instead of voucher_id (e.g., "5")
    db_item = OutvoucherItem(voucher_id=db_voucher.id, **item_data)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_outvoucher_by_id(db: Session, voucher_id: int):
    return db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()

def get_all_outvouchers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Outvoucher).offset(skip).limit(limit).all()

def update_outvoucher(db: Session, voucher_id: int, update_data: dict):
    outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not outvoucher:
        return None
    for key, value in update_data.items():
        setattr(outvoucher, key, value)
    db.commit()
    db.refresh(outvoucher)
    return outvoucher

def delete_outvoucher(db: Session, voucher_id: int):
    outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if outvoucher:
        db.delete(outvoucher)
        db.commit()
        return True
    return False
