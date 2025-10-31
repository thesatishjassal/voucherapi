import datetime
import shutil
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.quotation import Quotation as QuotationModel
from app.models.quotationitems import QuotationItem
from app.models.QuotationItemHistory import QuotationItemHistory
from app.schema.quotation import QuotationCreate
from app.schema.quotation_items import QuotationItemCreate
from typing import Optional

# ------------------------------------------------------
# Create New Quotation
# ------------------------------------------------------
def create_quotation(db: Session, quotation_data: QuotationCreate):
    quotation = QuotationModel(**quotation_data.dict())
    db.add(quotation)
    db.commit()
    db.refresh(quotation)
    return quotation

# ------------------------------------------------------
# Get Quotation by ID
# ------------------------------------------------------
def get_quotation_by_id(db: Session, quotation_id: int):
    return db.query(QuotationModel).filter(QuotationModel.id == quotation_id).first()

# ------------------------------------------------------
# Get All Quotations
# ------------------------------------------------------
def get_all_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(QuotationModel).order_by(desc(QuotationModel.id)).offset(skip).limit(limit).all()

# ------------------------------------------------------
# Update Quotation
# ------------------------------------------------------
def update_quotation(db: Session, quotation_id: int, update_data: dict):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        return None

    for key, value in update_data.items():
        setattr(quotation, key, value)

    db.commit()
    db.refresh(quotation)
    return quotation

# ------------------------------------------------------
# Delete Quotation
# ------------------------------------------------------
def delete_quotation(db: Session, quotation_id: int):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        return False

    # Delete all related items and histories
    db.query(QuotationItemHistory).filter(
        QuotationItemHistory.quotation_id == quotation_id
    ).delete()
    db.query(QuotationItem).filter(
        QuotationItem.quotation_id == quotation_id
    ).delete()
    db.delete(quotation)
    db.commit()
    return True

# ------------------------------------------------------
# Create Quotation Item
# ------------------------------------------------------
def create_quotation_item(db: Session, quotation_id: int, item_data: QuotationItemCreate):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    item = QuotationItem(**item_data.dict(), quotation_id=quotation_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# ------------------------------------------------------
# Get Items by Quotation ID
# ------------------------------------------------------
def get_items_by_quotation_id(db: Session, quotation_id: int):
    return db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).all()

# ------------------------------------------------------
# Update Single Quotation Item
# ------------------------------------------------------
def update_single_quotation_item(db: Session, quotation_id: int, item_id: int, item_data: QuotationItemCreate):
    item = db.query(QuotationItem).filter(
        QuotationItem.quotation_id == quotation_id,
        QuotationItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Quotation item not found")

    # Save current item to history before update
    history_entry = QuotationItemHistory(
        quotation_id=item.quotation_id,
        quotation_item_id=item.id,
        old_data=item.__dict__,
        changed_at=datetime.datetime.now()
    )
    db.add(history_entry)

    # Apply updates
    for key, value in item_data.dict().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

# ------------------------------------------------------
# Bulk Update Items
# ------------------------------------------------------
def bulk_update_quotation_items(db: Session, quotation_id: int, items_data: list):
    updated_items = []
    for item_data in items_data:
        item = db.query(QuotationItem).filter(
            QuotationItem.quotation_id == quotation_id,
            QuotationItem.id == item_data.id
        ).first()

        if item:
            for key, value in item_data.dict().items():
                setattr(item, key, value)
            db.add(item)
            updated_items.append(item)

    db.commit()
    return updated_items

# ------------------------------------------------------
# Add or Update Item Image
# ------------------------------------------------------
def add_or_update_item_image(db: Session, quotation_item_id: int, image_path: str):
    item = db.query(QuotationItem).filter(QuotationItem.id == quotation_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Quotation item not found")

    item.image = image_path
    db.commit()
    db.refresh(item)
    return item

# ------------------------------------------------------
# Delete Quotation Item
# ------------------------------------------------------
def delete_quotation_item(db: Session, item: QuotationItem):
    # Save deleted item in history
    history_entry = QuotationItemHistory(
        quotation_id=item.quotation_id,
        quotation_item_id=item.id,
        old_data=item.__dict__,
        changed_at=datetime.datetime.now(),
        action="deleted"
    )
    db.add(history_entry)
    db.delete(item)
    db.commit()
    return True

# ------------------------------------------------------
# Clone Quotation
# ------------------------------------------------------
def clone_quotation(db: Session, quotation_id: int):
    original = get_quotation_by_id(db, quotation_id)
    if not original:
        raise HTTPException(status_code=404, detail="Quotation not found")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_quotation_no = f"{original.quotation_no}-CLONE-{timestamp}"

    new_quotation = QuotationModel(
        **{col.name: getattr(original, col.name)
           for col in QuotationModel.__table__.columns if col.name != "id"},
        quotation_no=new_quotation_no
    )

    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)

    # Clone all items
    items = get_items_by_quotation_id(db, quotation_id)
    for item in items:
        cloned_item = QuotationItem(
            **{col.name: getattr(item, col.name)
               for col in QuotationItem.__table__.columns if col.name not in ["id", "quotation_id"]},
            quotation_id=new_quotation.id
        )
        db.add(cloned_item)
    db.commit()
    return new_quotation

# ------------------------------------------------------
# Create Quotation Revision
# ------------------------------------------------------
def create_quotation_revision(db: Session, quotation_id: int, update_data: Optional[dict] = None):
    original = get_quotation_by_id(db, quotation_id)
    if not original:
        raise HTTPException(status_code=404, detail="Quotation not found")

    base_no = original.quotation_no.split("-")[0]
    last_revision = db.query(QuotationModel).filter(
        QuotationModel.quotation_no.like(f"{base_no}-%")
    ).order_by(desc(QuotationModel.id)).first()

    if last_revision and "-" in last_revision.quotation_no:
        suffix = last_revision.quotation_no.split("-")[-1]
        if suffix.isalpha():
            new_suffix = chr(ord(suffix[-1]) + 1)
        else:
            new_suffix = "A"
    else:
        new_suffix = "A"

    new_quotation_no = f"{base_no}-{new_suffix}"

    new_quotation = QuotationModel(
        **{col.name: getattr(original, col.name)
           for col in QuotationModel.__table__.columns if col.name != "id"},
        quotation_no=new_quotation_no
    )

    if update_data:
        for key, value in update_data.items():
            setattr(new_quotation, key, value)

    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)

    # Duplicate all items
    items = get_items_by_quotation_id(db, quotation_id)
    for item in items:
        revised_item = QuotationItem(
            **{col.name: getattr(item, col.name)
               for col in QuotationItem.__table__.columns if col.name not in ["id", "quotation_id"]},
            quotation_id=new_quotation.id
        )
        db.add(revised_item)
    db.commit()
    return new_quotation

# ------------------------------------------------------
# Get All Item Histories
# ------------------------------------------------------
def get_all_quotation_item_histories(db: Session):
    return db.query(QuotationItemHistory).order_by(desc(QuotationItemHistory.changed_at)).all()

# ------------------------------------------------------
# Get History by Item ID
# ------------------------------------------------------
def get_history_by_quotation_item_id(db: Session, quotation_item_id: int):
    return db.query(QuotationItemHistory).filter(
        QuotationItemHistory.quotation_item_id == quotation_item_id
    ).order_by(desc(QuotationItemHistory.changed_at)).all()
