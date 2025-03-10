from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from app.models.quotation import Quotation  
from app.schema.quotation import QuotationCreate
from fastapi import HTTPException

def create_quotation(db: Session, quotation_data: QuotationCreate):
    new_quotation = Quotation(**quotation_data.dict())  # ✅ Use SQLAlchemy Model
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    return new_quotation

def get_quotation_by_id(db: Session, quotation_id: int):
    return db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()

def get_all_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quotation).offset(skip).limit(limit).all()  # ✅ Ensure Using Model

def update_quotation(db: Session, quotation_id: int, update_data: dict):
    quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
    if not quotation:
        return None
    for key, value in update_data.items():
        setattr(quotation, key, value)
    db.commit()
    db.refresh(quotation)
    return quotation

def delete_quotation(db: Session, quotation_id: int):
    quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
    if quotation:
        db.delete(quotation)
        db.commit()
        return True
    return False
