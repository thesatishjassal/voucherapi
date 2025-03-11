from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from app.models.products import Products
from app.models.quotation import Quotation  
from app.models.quotationitems import QuotationItem  
from app.schema.quotation import QuotationCreate
from app.schema.quotation_items import QuotationItemCreate
from fastapi import HTTPException

def create_quotation(db: Session, quotation_data: QuotationCreate):
    new_quotation = Quotation(**quotation_data.dict())  # ✅ Use SQLAlchemy Model
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    return new_quotation

def create_quotation_item(db: Session, quotation_id: int, item: QuotationItemCreate):
    try:
        with db.begin():
            db_quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
            if not db_quotation:
                raise HTTPException(status_code=404, detail="Quotation not found")

            product_id = item.product_id
            if not product_id:
                raise HTTPException(status_code=400, detail="Product ID is required")

            product = db.query(Products).filter(Products.itemcode == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with itemcode {product_id} not found")

            item_data = item.model_dump(exclude={"item_id", "quotation_id"})
            db_item = QuotationItem(quotation_id=db_quotation.quotation_id, **item_data)
            db.add(db_item)
            db.flush()  # Optional: Forces SQL to assign item_id
            db.refresh(db_item)  # ✅ Move inside transaction

        return db_item  # Now item_id is available and response will work
    except Exception as e:
        raise e  # Optional: handle/log as needed

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
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
