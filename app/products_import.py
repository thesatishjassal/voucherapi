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
    """Converts empty or invalid to None, preserves 'N/A' as 'N/A', else returns stripped string."""
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str == "":
        return None
    if val_str.lower() in ["none", "-"]:
        return None
    if val_str.lower() == "n/a":
        return "N/A"
    return val_str


def clean_numeric(val, default=0.0):
    """Cleans and converts to float, handling invalid values."""
    if val is None:
        return default
    val_str = str(val).strip()
    if val_str == "":
        return default
    if val_str.lower() in ["n/a", "na", "none", "-"]:
        return None  # For numerics, N/A to None
    # Remove common currency symbols
    val_str = val_str.replace("₹", "").replace("$", "").replace("€", "").replace("£", "").strip()
    try:
        num_val = float(val_str)
        return num_val
    except ValueError:
        return default


def clean_int(val, default=0):
    """Cleans and converts to int, handling invalid values."""
    if val is None:
        return default
    val_str = str(val).strip()
    if val_str == "":
        return default
    if val_str.lower() in ["n/a", "na", "none", "-"]:
        return default
    try:
        return int(float(val_str))  # Handles decimals by truncating
    except ValueError:
        return default


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

            # Handle boolean safely, default to True if invalid
            in_display_raw = row[18]
            in_display_value = str(in_display_raw).strip().lower() if in_display_raw else "true"
            if in_display_value in ["n/a", "na", "none", "-"]:
                in_display = True  # Default as per schema
            else:
                in_display = in_display_value in ["true", "yes", "1", "y"]

            # For reorderqty, default to 10 if 0 or invalid
            reorder_raw = row[20]
            reorder_cleaned = clean_int(reorder_raw, 10)

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
                "price": clean_numeric(row[10], 0.0),
                "quantity": clean_int(row[11], 0),
                "unit": clean_value(row[12]),
                "rackcode": clean_value(row[13]),
                "size": clean_value(row[14]),
                "cutoutdia": clean_value(row[15]),
                "category": clean_value(row[16]),
                "subcategory": clean_value(row[17]),
                "in_display": in_display,
                "model": clean_value(row[19]),
                "reorderqty": reorder_cleaned,
            }

            # Skip incomplete mandatory fields
            if not product_data_dict["itemcode"] or not product_data_dict["itemname"]:
                continue

            # Debug print: show first 3 rows
            if idx <= 5:
                print(f"Row {idx} raw: {row}")
                print(f"Row {idx} processed: {product_data_dict}")

            product_data = ProductsCreate(**product_data_dict)
            products_list.append(product_data)

        os.remove(temp_file_path)

        if not products_list:
            raise HTTPException(status_code=400, detail="No valid product data found in the file.")

        created_products = upload_products(products_list, db)
        return created_products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")