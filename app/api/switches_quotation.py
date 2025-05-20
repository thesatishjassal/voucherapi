from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schema.switchQuotation import SwitchQuotationSchema, SwitchQuotationCreate 
from app.controllers.SwitchQuotation import (
    create_switch_quotation,
    get_switch_quotation,
    get_switch_quotations,
    delete_switch_quotation,
    update_switch_quotation,
)
from database import get_db_connection

router = APIRouter(prefix="/switches_quotation", tags=["Switch Quotation"])


@router.post("/", response_model=SwitchQuotationSchema)
def create(data: SwitchQuotationCreate, db: Session = Depends(get_db_connection)):
    return create_switch_quotation(db=db, data=data)


@router.get("/", response_model=List[SwitchQuotationSchema])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)):
    return get_switch_quotations(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SwitchQuotationSchema)
def read_one(item_id: int, db: Session = Depends(get_db_connection)):
    item = get_switch_quotation(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db_connection)):
    deleted = delete_switch_quotation(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Deleted successfully"}


@router.put("/{item_id}", response_model=SwitchQuotationSchema)
def update(item_id: int, data: SwitchQuotationCreate, db: Session = Depends(get_db_connection)):
    updated = update_switch_quotation(db, item_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated
