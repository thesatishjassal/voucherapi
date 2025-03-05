from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.Outvoucher import create_outvoucher_item, create_outvoucher, get_all_outvouchers, get_outvoucher_by_id, update_outvoucher, delete_outvoucher
from app.schema.outvoucher import Outvoucher, OutvoucherCreate, OutvoucherBase
from app.schema.outvoucher_item import OutvoucherItem, OutvoucherItemCreate

app = FastAPI()
router = APIRouter()

@router.post("/outvouchers/", response_model=Outvoucher)
def create_voucher(outvoucher: OutvoucherCreate, db: Session = Depends(get_db_connection)):
    return create_outvoucher(db, outvoucher)

@router.post("/outvouchers/{voucher_id}/items/", response_model=OutvoucherItem)
def create_outvoucher_item_endpoint(voucher_id: int, item: OutvoucherItemCreate, db: Session = Depends(get_db_connection)):
    """Add an item to an existing invoucher."""
    return create_outvoucher_item(db, voucher_id, item)

@router.get("/outvouchers/{voucher_id}", response_model=Outvoucher)
def read_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    outvoucher = get_outvoucher_by_id(db, voucher_id)
    if not outvoucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return outvoucher

@router.get("/outvouchers/", response_model=list[Outvoucher])
def read_all_vouchers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_connection)):
    return get_all_outvouchers(db, skip, limit)

@router.put("/outvouchers/{voucher_id}", response_model=Outvoucher)
def update_voucher(voucher_id: int, update_data: dict, db: Session = Depends(get_db_connection)):
    updated_voucher = update_outvoucher(db, voucher_id, update_data)
    if not updated_voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return updated_voucher

@router.delete("/{voucher_id}")
def delete_voucher(voucher_id: int, db: Session = Depends(get_db_connection)):
    success = delete_outvoucher(db, voucher_id)
    if not success:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return {"message": "Voucher deleted successfully"}

# Include the router in the main app
app.include_router(router)