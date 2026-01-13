from sqlalchemy.orm import Session
from app.models.SwitchQuotationWa import SwitchQuotation
from app.schema.switchQuotation import SwitchQuotationCreate

def create_switch_quotation(db: Session, data: SwitchQuotationCreate):
    db_item = SwitchQuotation(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_switch_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SwitchQuotation).offset(skip).limit(limit).all()


def get_switch_quotation(db: Session, item_id: int):
    return db.query(SwitchQuotation).filter(SwitchQuotation.id == item_id).first()


def delete_switch_quotation(db: Session, item_id: int):
    item = get_switch_quotation(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item


def update_switch_quotation(db: Session, item_id: int, data: SwitchQuotationCreate):
    item = get_switch_quotation(db, item_id)
    if item:
        for key, value in data.dict().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item
