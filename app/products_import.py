from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openpyxl import load_workbook
from typing import List
from database import SessionLocal
from app.schema.products import ProductsResponse, ProductsCreate
from app.controllers.products import upload_products
import os

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

        products_list = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
            if all(cell is None for cell in row[:14]):  # Skip completely empty rows
                continue

            if any(cell is None for cell in row[:3]):  # Validate essential fields (hsncode, itemcode, itemname)
                continue  # Skip rows missing essential data

            # Map row to dictionary and handle possible None values safely
            product_data_dict = {
                "hsncode": str(row[0]).strip() if row[0] is not None else "",
                "itemcode": str(row[1]).strip() if row[1] is not None else "",
                "itemname": str(row[2]).strip() if row[2] is not None else "",
                "description": str(row[3]).strip() if row[3] is not None else "",
                "category": str(row[4]).strip() if row[4] is not None else "",
                "subcategory": str(row[5]).strip() if row[5] is not None else "",
                "price": float(row[6]) if row[6] is not None else 0.0,
                "quantity": int(row[7]) if row[7] is not None else 0,
                "rackcode": str(row[8]).strip() if row[8] is not None else "",
                "size": str(row[9]).strip() if row[9] is not None else "",
                "color": str(row[10]).strip() if row[10] is not None else "",
                "model": str(row[11]).strip() if row[11] is not None else "",
                "brand": str(row[12]).strip() if row[12] is not None else "",
                "unit": str(row[13]).strip() if row[13] is not None else "",
                "reorderqty": int(row[14]) if row[14] is not None else 10,
            }

            # Convert dict to Pydantic model
            product_data = ProductsCreate(**product_data_dict)

            # Append product to list
            products_list.append(product_data)

        # Remove temp file
        os.remove(temp_file_path)

        if not products_list:
            raise HTTPException(status_code=400, detail="No valid product data found in the file.")

        # Batch create products
        created_products = upload_products(products_list, db)

        return created_products

    except HTTPException as http_err:
        raise http_err  # Re-raise known HTTP errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
