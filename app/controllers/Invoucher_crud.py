from sqlalchemy.orm import Session
from app.models.invoucher import Invoucher as InvoucherModel
from app.schema.invoucher import Invoucher as InvoucherSchema, InvoucherCreate, InvoucherUpdate
from app.schema.invoucher_item import InvoucherItem as InvoucherItemSchema, InvoucherItemCreate
from app.models.invoucher_item import InvoucherItem
from fastapi import HTTPException
from typing import List

def create_invoucher(db: Session, invoucher: InvoucherCreate):
    """Create a new invoucher."""
    db_invoucher = InvoucherModel(**invoucher.model_dump())
    db.add(db_invoucher)
    db.commit()
    db.refresh(db_invoucher)
    # Return a dictionary including the id
    return {
        "id": db_invoucher.id,
        "voucher_id": db_invoucher.voucher_id,
        "voucher_number": db_invoucher.voucher_number,
        "transaction_type": db_invoucher.transaction_type,
        "voucher_date": db_invoucher.voucher_date,
        "client_id": db_invoucher.client_id,
        "invoice_number": db_invoucher.invoice_number,
        "invoice_date": db_invoucher.invoice_date,
        "mode_of_transport": db_invoucher.mode_of_transport,
        "number_of_packages": db_invoucher.number_of_packages,
        "freight_status": db_invoucher.freight_status,
        "total_amount": db_invoucher.total_amount,
        "remarks": db_invoucher.remarks
    }

def create_invoucher_item(db: Session, voucher_id: str, item: InvoucherItemCreate):
    """Create a new item for an invoucher using invouchers.id."""
    # Query by id instead of voucher_id
    db_voucher = db.query(InvoucherModel).filter(InvoucherModel.id == int(voucher_id)).first()
    if not db_voucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    
    item_data = item.model_dump(exclude={"item_id", "voucher_id"})
    # Use db_voucher.id (e.g., 48) instead of voucher_id (e.g., "5")
    db_item = InvoucherItem(voucher_id=db_voucher.id, **item_data)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Other functions remain unchanged
def get_invouchers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InvoucherModel).offset(skip).limit(limit).all()

def get_invoucher(db: Session, voucher_id: str):
    db_invoucher = db.query(InvoucherModel).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    return db_invoucher

def update_invoucher(db: Session, voucher_id: str, invoucher: InvoucherUpdate):
    db_invoucher = db.query(InvoucherModel).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    for key, value in invoucher.model_dump(exclude_unset=True).items():
        setattr(db_invoucher, key, value)
    db.commit()
    db.refresh(db_invoucher)
    return db_invoucher

def delete_invoucher(db: Session, voucher_id: str):
    db_invoucher = db.query(InvoucherModel).filter_by(voucher_id=voucher_id).first()
    if not db_invoucher:
        raise HTTPException(status_code=404, detail="Invoucher not found")
    db.delete(db_invoucher)
    db.commit()
    return {"message": "Invoucher deleted successfully"}

def get_items_by_voucher_id(db: Session, voucher_id: str) -> List[InvoucherItem]:
    items = db.query(InvoucherItem).filter(InvoucherItem.voucher_id == int(voucher_id)).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this voucher ID")
    return items