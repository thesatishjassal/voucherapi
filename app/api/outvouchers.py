from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.Outvoucher import (
    create_outvoucher,
    create_outvoucher_item,
    get_outvouchers,
    get_outvoucher,
    update_outvoucher,
    delete_outvoucher,
    get_items_by_voucher_id
)
from app.schema.outvoucher import Outvoucher, OutvoucherCreate, OutvoucherUpdate
from app.schema.outvoucher_item import OutvoucherItem, OutvoucherItemCreate
from typing import List
from app.schema.outvoucher_item import OutvoucherItem as OutvoucherItemSchema

app = FastAPI()
router = APIRouter()

# **Outvoucher Endpoints**
@router.post("/outvouchers/", response_model=Outvoucher)
def create_outvoucher_endpoint(outvoucher: OutvoucherCreate, db: Session = Depends(get_db_connection)):
    """Create a new outvoucher."""
    return create_outvoucher(db, outvoucher)

@router.post("/outvouchers/{voucher_id}/items/", response_model=OutvoucherItem)
def create_outvoucher_item_endpoint(voucher_id: int, item: OutvoucherItemCreate, db: Session = Depends(get_db_connection)):
    """Add an item to an existing outvoucher."""
    return create_outvoucher_item(db, voucher_id, item)

@router.get("/outvouchers/", response_model=List[Outvoucher])
def read_outvouchers_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    """List all outvouchers with pagination."""
    return get_outvouchers(db, skip, limit)

@router.get("/outvouchers/{voucher_id}", response_model=Outvoucher)
def read_outvoucher_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Retrieve a specific outvoucher by ID."""
    return get_outvoucher(db, voucher_id)

@router.put("/outvouchers/{voucher_id}", response_model=Outvoucher)
def update_outvoucher_endpoint(voucher_id: int, outvoucher: OutvoucherUpdate, db: Session = Depends(get_db_connection)):
    """Update an existing outvoucher."""
    return update_outvoucher(db, voucher_id, outvoucher)

@router.delete("/outvouchers/{voucher_id}")
def delete_outvoucher_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Delete an outvoucher."""
    return delete_outvoucher(db, voucher_id)

@router.get("/outvouchers/{voucher_id}/items/", response_model=List[OutvoucherItemSchema])
def read_outvoucher_items_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Retrieve all items for a specific outvoucher by voucher ID."""
    return get_items_by_voucher_id(db, voucher_id)

app.include_router(router)
