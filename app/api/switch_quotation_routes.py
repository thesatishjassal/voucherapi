from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_connection
from app.schema.switch_quotation_wa import SwitchQuotationCreate
from app.controllers.switch_quotation_controller import (
    create_switch_quotation,
    get_all_switch_quotations,
    get_switch_quotation_by_id,
    update_switch_quotation,
    delete_switch_quotation
)

router = APIRouter(
    prefix="/switch-quotations",
    tags=["Switch Quotations"]
)


# CREATE
@router.post("/", status_code=201)
def create(payload: SwitchQuotationCreate, db: Session = Depends(get_db_connection)):
    quotation = create_switch_quotation(db, payload)
    return {"success": True, "quotation_id": quotation.quotation_id}


# READ ALL
@router.get("/")
def get_all(db: Session = Depends(get_db_connection)):
    return get_all_switch_quotations(db)


# READ ONE
@router.get("/{quotation_id}")
def get_one(quotation_id: int, db: Session = Depends(get_db_connection)):
    quotation = get_switch_quotation_by_id(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation


# UPDATE
@router.put("/{quotation_id}")
def update(
    quotation_id: int,
    payload: SwitchQuotationCreate,
    db: Session = Depends(get_db_connection)
):
    quotation = update_switch_quotation(db, quotation_id, payload)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"success": True, "message": "Quotation updated"}


# DELETE
@router.delete("/{quotation_id}")
def delete(quotation_id: int, db: Session = Depends(get_db_connection)):
    success = delete_switch_quotation(db, quotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return {"success": True, "message": "Quotation deleted"}
