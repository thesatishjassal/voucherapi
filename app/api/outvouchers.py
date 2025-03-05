from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db_connection
from app.schema.outvoucher import Outvoucher, OutvoucherCreate, OutvoucherUpdate
from app.schema.outvoucher_item import OutvoucherItemCreate, OutvoucherItem
from app.controllers.Outvoucher import (
    create_outvoucher, get_outvouchers, get_outvoucher_by_id, 
    update_outvoucher, delete_outvoucher, get_outvoucher_items_by_voucher_id,
    create_outvoucher_item
)

app = FastAPI()
router = APIRouter()

@router.post("/outvouchers/", response_model=Outvoucher)
def create_voucher(outvoucher: OutvoucherCreate, db: Session = Depends(get_db_connection)):
    return create_outvoucher(db, outvoucher)

@router.get("/outvouchers/", response_model=List[Outvoucher])
def read_all_vouchers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    return get_outvouchers(db, skip, limit)

@router.get("/outvouchers/{voucher_id}", response_model=Outvoucher)
def read_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    return get_outvoucher_by_id(db, voucher_id)

@router.put("/outvouchers/{voucher_id}", response_model=Outvoucher)
def update_voucher(voucher_id: int, update_data: OutvoucherUpdate, db: Session = Depends(get_db_connection)):
    return update_outvoucher(db, voucher_id, update_data)

@router.delete("/outvouchers/{voucher_id}")
def delete_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    return delete_outvoucher(db, voucher_id)

@router.post("/outvouchers/{voucher_id}/items/", response_model=OutvoucherItem)
def create_voucher_item(voucher_id: int, item: OutvoucherItemCreate, db: Session = Depends(get_db_connection)):
    return create_outvoucher_item(db, voucher_id, item)

@router.get("/outvouchers/{voucher_id}/items/", response_model=List[OutvoucherItem])
def read_voucher_items(voucher_id: int, db: Session = Depends(get_db_connection)):
    return get_outvoucher_items_by_voucher_id(db, voucher_id)

# Include the router in the main app
app.include_router(router)
