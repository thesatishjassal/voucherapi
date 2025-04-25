from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# Removed unused import: Products
from app.schema.products import ProductsCreate
import csv
import io
from typing import List
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_csv(file: UploadFile, db: Session):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = file.file.read()
        csv_file = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)

        # Log the field names to ensure the CSV is parsed correctly
        logger.info(f"CSV columns: {csv_reader.fieldnames}")

        products_data: List[ProductsCreate] = []
        failed_rows = []
        row_count = 0

        for row_num, row in enumerate(csv_reader, start=1):
            row_count += 1
            try:
                # Ensure all required fields are present
                required_fields = ['hsncode', 'itemcode', 'itemname', 'description', 'category', 'subcategory', 'price', 'quantity', 'rackcode', 'size', 'color', 'model', 'brand', 'unit', 'reorderqty']
                for field in required_fields:
                    if field not in row or not row[field].strip():
                        raise ValueError(f"Missing or empty field: {field}")

                # Explicit type conversion with logging
                price = float(row['price'])
                quantity = int(row['quantity'])
                reorderqty = int(row['reorderqty']) if row['reorderqty'].strip() else 0

                logger.info(f"Row {row_num} - price: {price} (type: {type(price)}), quantity: {quantity} (type: {type(quantity)}), reorderqty: {reorderqty} (type: {type(reorderqty)})")

                product_data = ProductsCreate(
                    hsncode=row['hsncode'],
                    itemcode=row['itemcode'],
                    itemname=row['itemname'],
                    description=row['description'],
                    category=row['category'],
                    subcategory=row['subcategory'],
                    price=price,
                    quantity=quantity,
                    rackcode=row['rackcode'],
                    size=row['size'],
                    color=row['color'],
                    model=row['model'],
                    brand=row['brand'],
                    unit=row['unit'],
                    reorderqty=reorderqty
                )
                products_data.append(product_data)
            except (ValueError, KeyError) as e:
                logger.error(f"Row {row_num} failed: {str(e)} - Row data: {row}")
                failed_rows.append({"row": row_num, "error": str(e), "data": row})

        logger.info(f"Total rows read from CSV: {row_count}")
        logger.info(f"Successfully parsed rows: {len(products_data)}")
        logger.info(f"Failed rows: {len(failed_rows)}")

        if not products_data:
            raise HTTPException(
                status_code=400,
                detail=f"No valid rows found in CSV. Failed rows: {failed_rows}"
            )

        # Process in batches of 10 to isolate issues
        BATCH_SIZE = 10
        uploaded_count = 0
        batch_failed_rows = []

        from app.controllers.products import upload_products
        for i in range(0, len(products_data), BATCH_SIZE):
            batch = products_data[i:i + BATCH_SIZE]
            try:
                result = upload_products(batch, db)
                uploaded_count += len(batch) if isinstance(result, list) else 1
            except HTTPException as e:
                logger.error(f"Batch {i//BATCH_SIZE + 1} failed: {str(e.detail)}")
                batch_failed_rows.append({"batch": i//BATCH_SIZE + 1, "error": str(e.detail)})

        response = {
            "message": "CSV data processed",
            "total_rows": row_count,
            "successful_uploads": uploaded_count,
            "failed_rows": failed_rows,
            "batch_errors": batch_failed_rows
        }

        if uploaded_count == 0:
            raise HTTPException(status_code=400, detail=response)

        return JSONResponse(status_code=200, content=response)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid data format in CSV: " + str(ve))
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))