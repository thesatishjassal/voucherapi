from sqlite3 import IntegrityError
from typing import List
from sqlalchemy.orm import Session
from app.models.products import Products
from app.models.quotation import Quotation  
from app.models.quotationitems import QuotationItem  
from app.schema.quotation import QuotationCreate
from app.schema.quotation_items import QuotationItemCreate, QuotationItemResponse, QuotationItemBase
from fastapi import HTTPException

def create_quotation(db: Session, quotation_data: QuotationCreate):
    new_quotation = Quotation(**quotation_data.dict())  # ✅ Use SQLAlchemy Model
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    return new_quotation

def create_quotation_item(db: Session, quotation_id: int, item: QuotationItemCreate) -> QuotationItemResponse:
    try:
        with db.begin():  # Start transaction
            # 🔍 Check if the quotation exists
            db_quotation = db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()
            if not db_quotation:
                raise HTTPException(status_code=404, detail="Quotation not found")

            # 🔍 Validate product_id
            product_id = item.product_id
            if not product_id:
                raise HTTPException(status_code=400, detail="Product ID is required")

            # 🔍 Check if product exists
            product = db.query(Products).filter(Products.itemcode == product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with itemcode '{product_id}' not found"
                )

            # ✅ Prepare data and exclude 'item_id', 'quotation_id' (quotation_id will be added separately)
            item_data = item.model_dump(exclude={"item_id", "quotation_id"})

            # 💾 Create and add the new QuotationItem
            db_item = QuotationItem(quotation_id=db_quotation.quotation_id, **item_data)
            db.add(db_item)
            db.flush()  # Get auto-generated ID
            db.refresh(db_item)  # Refresh to get the latest DB state

        # ✅ Return the response schema (automatically maps 'id' to 'item_id' in response)
        return QuotationItemResponse(
            item_id=db_item.id,  # map id -> item_id
            quotation_id=db_item.quotation_id,
            product_id=db_item.product_id,
            customercode=db_item.customercode,
            customerdescription=db_item.customerdescription,
            image=db_item.image,
            itemcode=db_item.itemcode,
            brand=db_item.brand,
            mrp=db_item.mrp,
            price=db_item.price,
            quantity=db_item.quantity,
            discount=db_item.discount,
            item_name=db_item.item_name,
            unit=db_item.unit
        )

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e.orig}")

    except HTTPException:
        raise  # Re-raise HTTPExceptions without modification

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_items_by_quotation_id(db: Session, quotation_id: str) -> List[QuotationItem]:
    items = db.query(QuotationItem).filter(QuotationItem.quotation_id == int(quotation_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this quotation id")
    return items
    
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
