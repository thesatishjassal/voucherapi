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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clean_value(val):
    """Converts Excel 'N/A' or empty to None, else returns stripped string."""
    if val is None:
        return None
    val = str(val).strip()
    if val.lower() in ["n/a", "na", "none", "-", ""]:
        return None
    return val


@router.post("/import-products/", response_model=List[ProductsResponse])
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Imports products from Excel into DB.
    Expected order:
    itemcode, itemname, description, brand, watt, color, cct, beamangle, cri, lumens,
    price, quantity, unit, rackcode, size, cutoutdia, category, subcategory,
    in_display, model, reorderqty
    """

    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

    try:
        contents = await file.read()
        temp_file_path = "temp_import.xlsx"
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        workbook = load_workbook(filename=temp_file_path)
        sheet = workbook.active

        products_list = []

        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if all(cell is None for cell in row):
                continue

            # Handle boolean safely
            in_display_value = str(row[18]).strip().lower() if row[18] else "true"
            in_display = in_display_value in ["true", "yes", "1", "y"]

            product_data_dict = {
                "itemcode": clean_value(row[0]),
                "itemname": clean_value(row[1]),
                "description": clean_value(row[2]),
                "brand": clean_value(row[3]),
                "watt": clean_value(row[4]),
                "color": clean_value(row[5]),
                "cct": clean_value(row[6]),
                "beamangle": clean_value(row[7]),
                "cri": clean_value(row[8]),
                "lumens": clean_value(row[9]),
                "price": float(row[10]) if row[10] else 0.0,
                "quantity": int(row[11]) if row[11] else 0,
                "unit": clean_value(row[12]),
                "rackcode": clean_value(row[13]),
                "size": clean_value(row[14]),
                "cutoutdia": clean_value(row[15]),
                "category": clean_value(row[16]),
                "subcategory": clean_value(row[17]),
                "in_display": in_display,
                "model": clean_value(row[19]),
                "reorderqty": int(row[20]) if row[20] else 10,
            }

            # Skip incomplete mandatory fields
            if not product_data_dict["itemcode"] or not product_data_dict["itemname"]:
                continue

            # Debug print: show first 3 rows
            if idx <= 5:
                print(f"Row {idx} -> {product_data_dict}")

            product_data = ProductsCreate(**product_data_dict)
            products_list.append(product_data)

        os.remove(temp_file_path)

        if not products_list:
            raise HTTPException(status_code=400, detail="No valid product data found in the file.")

        created_products = upload_products(products_list, db)
        return created_products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
