from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openpyxl import load_workbook
from typing import List
from database import SessionLocal
from app.schema.products import ProductsResponse
from app.controllers.products import create_products

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/import-products/", response_model=List[ProductsResponse])
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

    try:
        contents = await file.read()
        with open("temp.xlsx", "wb") as f:
            f.write(contents)

        workbook = load_workbook(filename="temp.xlsx")
        sheet = workbook.active

        products = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping header
            if any(cell is None for cell in row[:14]):  # Validate essential columns
                continue

            product_data = {
                "hsncode": str(row[0]),
                "itemcode": str(row[1]),
                "itemname": str(row[2]),
                "description": str(row[3]),
                "category": str(row[4]),
                "subcategory": str(row[5]),
                "price": float(row[6]),
                "quantity": int(row[7]),
                "rackcode": str(row[8]),
                "size": str(row[9]),
                "color": str(row[10]),
                "model": str(row[11]),
                "brand": str(row[12]),
                "unit": str(row[13]),
            }

            db_product = create_products(db, product_data)
            products.append(db_product)

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
