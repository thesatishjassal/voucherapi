from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openpyxl import load_workbook
from typing import List
from database import SessionLocal
from app.schema.products import ProductsResponse, ProductsCreate
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
        # Save the uploaded file temporarily
        contents = await file.read()
        temp_file_path = "temp.xlsx"
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        # Load workbook
        workbook = load_workbook(filename=temp_file_path)
        sheet = workbook.active

        products = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
            if any(cell is None for cell in row[:14]):  # Validate essential columns
                continue  # Skip rows with missing essential data

            # Map row to dictionary and handle possible None values safely
            product_data_dict = {
                "hsncode": str(row[0]).strip(),
                "itemcode": str(row[1]).strip(),
                "itemname": str(row[2]).strip(),
                "description": str(row[3]).strip(),
                "category": str(row[4]).strip(),
                "subcategory": str(row[5]).strip(),
                "price": float(row[6]) if row[6] is not None else 0.0,
                "quantity": int(row[7]) if row[7] is not None else 0,
                "rackcode": str(row[8]).strip(),
                "size": str(row[9]).strip(),
                "color": str(row[10]).strip(),
                "model": str(row[11]).strip(),
                "brand": str(row[12]).strip(),
                "unit": str(row[13]).strip(),
            }

            # Convert dict to Pydantic model
            product_data = ProductsCreate(**product_data_dict)

            # Call the product creation function
            db_product = create_products(product_data, db)
            products.append(db_product)

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
