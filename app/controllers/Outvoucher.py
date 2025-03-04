from sqlalchemy.orm import Session
from app.models.outvocher import Outvoucher
from app.models.outvoucher_item import OutvoucherItem
from app.schema.outvoucher import OutvoucherCreate, OutvoucherUpdate
from app.schema.outvoucher_item import OutvoucherItemCreate

def create_outvoucher(db: Session, outvoucher_data: OutvoucherCreate):
    new_outvoucher = Outvoucher(**outvoucher_data.dict())
    db.add(new_outvoucher)
    db.commit()
    db.refresh(new_outvoucher)
    return new_outvoucher

def create_outvoucher_item(db: Session, voucher_id: int, item_data: OutvoucherItemCreate):
    new_item = OutvoucherItem(voucher_id=voucher_id, **item_data.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_outvoucher(db: Session, voucher_id: int):
    return db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()

def get_outvouchers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Outvoucher).offset(skip).limit(limit).all()

def update_outvoucher(db: Session, voucher_id: int, update_data: OutvoucherUpdate):
    outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if not outvoucher:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(outvoucher, key, value)
    db.commit()
    db.refresh(outvoucher)
    return outvoucher

def delete_outvoucher(db: Session, voucher_id: int):
    outvoucher = db.query(Outvoucher).filter(Outvoucher.id == voucher_id).first()
    if outvoucher:
        db.delete(outvoucher)
        db.commit()
        return {"message": "Outvoucher deleted successfully"}
    return {"error": "Outvoucher not found"}

def get_items_by_voucher_id(db: Session, voucher_id: int):
    return db.query(OutvoucherItem).filter(OutvoucherItem.voucher_id == voucher_id).all()
