from sqlalchemy.orm import Session
from app.models.outvocher import Outvoucher
from schema import outvoucher, outvoucher_item

def create_outvoucher(db: Session, outvoucher_data: outvoucher.OutvoucherCreate):
    new_outvoucher = Outvoucher(**outvoucher_data.dict())
    db.add(new_outvoucher)
    db.commit()
    db.refresh(new_outvoucher)
    return new_outvoucher

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
