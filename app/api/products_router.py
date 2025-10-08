# app/routers/products_router.py
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.update_products_from_csv import update_products_from_csv

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/update-csv")
def update_products_csv(file: UploadFile = UploadFile(...), db: Session = Depends(get_db_connection)):
    """
    Upload CSV to update existing products
    """
    return update_products_from_csv(file, db)
