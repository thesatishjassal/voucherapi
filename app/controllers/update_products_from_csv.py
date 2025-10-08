# app/controllers/products_controller.py
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.products import Products
import csv
import io
import logging

logger = logging.getLogger(__name__)

def update_products_from_csv(file: UploadFile, db: Session):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = file.file.read()
    csv_file = io.StringIO(contents.decode('utf-8'))
    reader = csv.DictReader(csv_file)

    updated_count = 0
    failed_rows = []

    for row_num, row in enumerate(reader, start=1):
        try:
            itemcode = row.get('itemcode')
            if not itemcode:
                raise ValueError("Missing itemcode")

            product = db.query(Products).filter(Products.itemcode == itemcode).first()
            if not product:
                raise ValueError(f"Product with itemcode {itemcode} not found")

            # Update fields if present
            product.cct = row.get('cct', product.cct)
            product.beamangle = row.get('beamangle', product.beamangle)
            product.cutoutdia = row.get('cutoutdia', product.cutoutdia)
            product.cri = row.get('cri', product.cri)
            product.lumens = row.get('lumens', product.lumens)
            product.watt = row.get('watt', product.watt)

            in_display_val = row.get('in_display')
            if in_display_val is not None:
                product.in_display = str(in_display_val).strip().lower() in ('true', '1', 'yes')

            updated_count += 1

        except Exception as e:
            logger.error(f"Row {row_num} failed: {str(e)}")
            failed_rows.append({"row": row_num, "error": str(e), "data": row})

    db.commit()

    return JSONResponse(status_code=200, content={
        "message": f"Products updated successfully: {updated_count}",
        "failed_rows": failed_rows
    })
