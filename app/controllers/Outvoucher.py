from sqlite3 import IntegrityError
from typing import List
from sqlalchemy.orm import Session
from app.models.outvoucher import Outvoucher  # ✅ SQLAlchemy Model
from app.models.outvoucher_item import OutvoucherItem  # ✅ SQLAlchemy Model
from app.schema.outvoucher import OutvoucherCreate  # ✅ Pydantic Schema
from app.models.products import Products  # ✅ Pydantic Schema
from app.schema.outvoucher_item import OutvoucherItemCreate  # ✅ Pydantic Schema
from fastapi import HTTPException

def create_outvoucher(db: Session, outvoucher_data: OutvoucherCreate):
    new_outvoucher = Outvoucher(**outvoucher_data.dict())  # ✅ Use SQLAlchemy Model
    db.add(new_outvoucher)
    db.commit()
    db.refresh(new_outvoucher)
    return new_outvoucher

def create_outvoucher_item(db: Session, voucher_id: int, item: OutvoucherItemCreate):
    try:
        with db.begin():
            db_voucher = db.query(Outvoucher).filter(Outvoucher.voucher_id == voucher_id).first()
            if not db_voucher:
                raise HTTPException(status_code=404, detail="Voucher not found")
            product_id = item.product_id
            if not product_id:
                raise HTTPException(status_code=400, detail="Product ID is required")
            
            product = db.query(Products).filter(Products.itemcode == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with itemcode {product_id} not found")
            
            item_data = item.model_dump(exclude={"item_id", "voucher_id"})
            db_item = OutvoucherItem(voucher_id=db_voucher.voucher_id, **item_data)
            db.add(db_item)
        #  the inxstance outside the transaction context if needed
        db.refresh(db_item)
        return db_item

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
def get_items_by_voucher_id(db: Session, voucher_id: str) -> List[OutvoucherItem]:
    items = db.query(OutvoucherItem).filter(OutvoucherItem.voucher_id == int(voucher_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this voucher ID")
    return items

def get_outvoucher_by_id(db: Session, voucher_id: int):
    return db.query(Outvoucher).filter(Outvoucher.voucher_id == voucher_id).first()

def get_all_outvouchers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Outvoucher).offset(skip).limit(limit).all()  # ✅ Ensure Using Model

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
