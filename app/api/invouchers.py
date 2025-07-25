from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.Invoucher_crud import get_items_by_voucher_id, create_invoucher, create_invoucher_item, get_invouchers, get_invoucher, update_invoucher, delete_invoucher
from app.schema.invoucher import Invoucher, InvoucherCreate, InvoucherUpdate
from app.schema.invoucher_item import InvoucherItem, InvoucherItemCreate, InvoucherItemResponse
from typing import List
# from app.schema.invoucher_item import InvoucherItem as InvoucherItemResponse

app = FastAPI()
router = APIRouter()

# Invoucher Endpoints
@router.post("/invouchers/", response_model=Invoucher)
def create_invoucher_endpoint(invoucher: InvoucherCreate, db: Session = Depends(get_db_connection)):
    """Create a new invoucher."""
    return create_invoucher(db, invoucher)

@router.post("/invouchers/{voucher_id}/items/", response_model=InvoucherItem)
def create_invoucher_item_endpoint(voucher_id: int, item: InvoucherItemCreate, db: Session = Depends(get_db_connection)):
    """Add an item to an existing invoucher."""
    return create_invoucher_item(db, voucher_id, item)

@router.get("/invouchers/", response_model=List[Invoucher])
def read_invouchers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_connection)):
    """List all invouchers with pagination."""
    return get_invouchers(db, skip, limit)

@router.get("/invouchers/{voucher_id}", response_model=Invoucher)
def read_invoucher_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Retrieve a specific invoucher by ID."""
    return get_invoucher(db, voucher_id)

@router.put("/invouchers/{voucher_id}", response_model=Invoucher)
def update_invoucher_endpoint(voucher_id: int, invoucher: InvoucherCreate, db: Session = Depends(get_db_connection)):
    """Update an existing invoucher."""
    return update_invoucher(db, voucher_id, invoucher)

@router.delete("/invouchers/{voucher_id}")
def delete_invoucher_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Delete an invoucher."""
    return delete_invoucher(db, voucher_id)

@router.get("/invouchers/{voucher_id}/items/", response_model=List[InvoucherItemResponse])
def read_invoucher_items_endpoint(voucher_id: int, db: Session = Depends(get_db_connection)):
    """Retrieve all items for a specific invoucher by voucher ID."""
    return get_items_by_voucher_id(db, voucher_id)

app.include_router(router)
