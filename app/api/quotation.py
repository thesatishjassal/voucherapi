from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.quotation import create_quotation_item, create_quotation, get_quotation_by_id, get_all_quotations, update_quotation, delete_quotation
from app.schema.quotation import Quotation, QuotationCreate
from app.schema.quotation_items import QuotationItem, QuotationItemCreate

app = FastAPI()
router = APIRouter()

@router.post("/quotation/", response_model=Quotation)
def create_quotation_api(quotation: QuotationCreate, db: Session = Depends(get_db_connection)):
    return create_quotation(db, quotation)

@router.post("/quotation/{quotation_id}/items/", response_model=QuotationItem)
def create_outoucher_item_endpoint(quotation_id: int, item: QuotationItemCreate, db: Session = Depends(get_db_connection)):
    """Add an item to an existing invoucher."""
    return create_quotation_item(db, quotation_id, item)


@router.get("/quotation/{quotation_id}", response_model=Quotation)
def read_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    quotation = get_quotation_by_id(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

@router.get("/quotation/", response_model=list[Quotation])
def read_all_quotation(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)):
    return get_all_quotations(db, skip, limit)

@router.put("/quotation/{quotation_id}", response_model=Quotation)
def update_quotation_api(quotation_id: int, update_data: dict, db: Session = Depends(get_db_connection)):
    updated_quotation = update_quotation(db, quotation_id, update_data)
    if not updated_quotation:
        raise HTTPException(status_code=404, detail="quotation not found")
    return updated_quotation

@router.delete("/{quotation_id}")
def delete_quotation_api(quotation_id: int, db: Session = Depends(get_db_connection)):
    success = delete_quotation(db, quotation_id)
    if not success:
        raise HTTPException(status_code=404, detail="quotation not found")
    return {"message": "quotation deleted successfully"}


# Include the router in the main app
app.include_router(router)