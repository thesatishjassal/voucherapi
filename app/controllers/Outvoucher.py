from sqlalchemy.orm import Session
from app.schema.outvoucher import OutvoucherCreate, OutvoucherUpdate
from app.models.outvoucher import Outvoucher
from app.models.outvoucher_item import OutvoucherItem
from app.schema.outvoucher_item import OutvoucherItemCreate, OutvoucherItem
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
