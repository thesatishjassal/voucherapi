from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openpyxl import load_workbook
from typing import List
from database import SessionLocal
from app.schema.products import ProductsResponse, ProductsCreate
from app.controllers.products import upload_products
import os

router = APIRouter()


# -------------------- Database Dependency --------------------
def get_db():
    """Dependency for DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Excel Import API --------------------
@router.post("/import-products/", response_model=List[ProductsResponse])
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Imports products from Excel into the database.

    Expected Excel columns (in this exact order):
    itemcode, itemname, description, brand, watt, color, cct, beamangle, cri, lumens,
    price, quantity, unit, rackcode, size, cutoutdia, category, subcategory,
    in_display, model, reorderqty
    """

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

    try:
        # Save the uploaded file temporarily
        contents = await file.read()
        temp_file_path = "temp_import.xlsx"
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        workbook = load_workbook(filename=temp_file_path)
        sheet = workbook.active

        products_list = []

        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
            if all(cell is None for cell in row):
                continue  # skip empty rows

            # Handle boolean conversion for in_display
            in_display_value = str(row[18]).strip().lower() if row[18] is not None else "true"
            in_display = in_display_value in ["true", "yes", "1", "y"]

            product_data_dict = {
                "itemcode": str(row[0]).strip() if row[0] else "",
                "itemname": str(row[1]).strip() if row[1] else "",
                "description": str(row[2]).strip() if row[2] else "",
                "brand": str(row[3]).strip() if row[3] else "",
                "watt": str(row[4]).strip() if row[4] else "",
                "color": str(row[5]).strip() if row[5] else "",
                "cct": str(row[6]).strip() if row[6] else "",
                "beamangle": str(row[7]).strip() if row[7] else "",
                "cri": str(row[8]).strip() if row[8] else "",
                "lumens": str(row[9]).strip() if row[9] else "",
                "price": float(row[10]) if row[10] else 0.0,
                "quantity": int(row[11]) if row[11] else 0,
                "unit": str(row[12]).strip() if row[12] else "",
                "rackcode": str(row[13]).strip() if row[13] else "",
                "size": str(row[14]).strip() if row[14] else "",
                "cutoutdia": str(row[15]).strip() if row[15] else "",
                "category": str(row[16]).strip() if row[16] else "",
                "subcategory": str(row[17]).strip() if row[17] else "",
                "in_display": in_display,
                "model": str(row[19]).strip() if row[19] else "",
                "reorderqty": int(row[20]) if row[20] else 10,
            }

            # Skip incomplete mandatory fields
            if not product_data_dict["itemcode"] or not product_data_dict["itemname"]:
                continue

            product_data = ProductsCreate(**product_data_dict)
            products_list.append(product_data)

        # Remove temporary file
        os.remove(temp_file_path)

        if not products_list:
            raise HTTPException(status_code=400, detail="No valid product data found in the file.")

        # Insert into DB
        created_products = upload_products(products_list, db)
        return created_products

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
