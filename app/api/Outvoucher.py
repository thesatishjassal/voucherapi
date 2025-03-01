from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.controllers.Outvoucher import create_outvoucher, update_outvoucher, get_all_outvouchers, get_outvoucher_by_id, delete_outvoucher
from app.schema.outvoucher import OutvoucherCreate, OutvoucherResponse

router = APIRouter(prefix="/outvouchers", tags=["Outvouchers"])

@router.post("/", response_model=OutvoucherResponse)
def create_voucher(outvoucher: OutvoucherCreate, db: Session = Depends(get_db)):
    return create_outvoucher(db, outvoucher)

@router.get("/{voucher_id}", response_model=OutvoucherResponse)
def read_voucher(voucher_id: int, db: Session = Depends(get_db)):
    outvoucher = get_outvoucher_by_id(db, voucher_id)
    if not outvoucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return outvoucher

@router.get("/", response_model=list[OutvoucherResponse])
def read_all_vouchers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_outvouchers(db, skip, limit)

@router.put("/{voucher_id}", response_model=OutvoucherResponse)
def update_voucher(voucher_id: int, update_data: dict, db: Session = Depends(get_db)):
    updated_voucher = update_outvoucher(db, voucher_id, update_data)
    if not updated_voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return updated_voucher

@router.delete("/{voucher_id}")
def delete_voucher(voucher_id: int, db: Session = Depends(get_db)):
    success = delete_outvoucher(db, voucher_id)
    if not success:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return {"message": "Voucher deleted successfully"}
