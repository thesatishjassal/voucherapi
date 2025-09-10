from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from openpyxl import load_workbook
from typing import List
from database import SessionLocal
from app.schema.products import ProductsResponse, ProductsCreate
from app.controllers.products import upload_products
import os

router = APIRouter()


def get_db():
    """Dependency for DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/import-products/", response_model=List[ProductsResponse])
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Imports products from an uploaded Excel (.xlsx or .xls) file into the database.

    Expects the following columns in order:
    itemcode, itemname, description, category, subcategory, price,
    quantity, rackcode, size, color, model, brand, unit, reorderqty, cct, beamangle, cutoutdia
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

    try:
        # Save the uploaded file temporarily
        contents = await file.read()
        temp_file_path = "temp.xlsx"
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        workbook = load_workbook(filename=temp_file_path)
        sheet = workbook.active

        products_list = []

        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
            if all(cell is None for cell in row[:18]):  # check first 18 cols (updated count)
                continue

            if any(cell is None for cell in row[:3]):  # require hsncode, itemcode, itemname
                continue

            product_data_dict = {
                # "hsncode": str(row[0]).strip() if row[0] else "",
                "itemcode": str(row[1]).strip() if row[1] else "",
                "itemname": str(row[2]).strip() if row[2] else "",
                "description": str(row[3]).strip() if row[3] else "",
                "category": str(row[4]).strip() if row[4] else "",
                "subcategory": str(row[5]).strip() if row[5] else "",
                "price": float(row[6]) if row[6] else 0.0,
                "quantity": int(row[7]) if row[7] else 0,
                "rackcode": str(row[8]).strip() if row[8] else "",
                "size": str(row[9]).strip() if row[9] else "",
                "color": str(row[10]).strip() if row[10] else "",
                "model": str(row[11]).strip() if row[11] else "",
                "brand": str(row[12]).strip() if row[12] else "",
                "unit": str(row[13]).strip() if row[13] else "",
                "watt": str(row[13]).strip() if row[13] else "",
                "reorderqty": int(row[14]) if row[14] else 10,
                "cct": str(row[15]).strip() if row[15] else None,
                "beamangle": str(row[16]).strip() if row[16] else None,
                "cutoutdia": str(row[17]).strip() if row[17] else None,
                "cri": str(row[16]).strip() if row[16] else None,
                "lumens": str(row[17]).strip() if row[17] else None,
                "in_display": str(row[17]).strip() if row[17] else None,
            }

            product_data = ProductsCreate(**product_data_dict)
            products_list.append(product_data)

        os.remove(temp_file_path)

        if not products_list:
            raise HTTPException(status_code=400, detail="No valid product data found in the file.")

        created_products = upload_products(products_list, db)
        return created_products

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
