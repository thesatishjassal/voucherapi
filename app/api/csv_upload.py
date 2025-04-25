from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.products import Products
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

                # Explicit type conversion with validation
                price = float(row['price'])
                quantity = int(row['quantity'])
                reorderqty = int(row['reorderqty']) if row['reorderqty'].strip() else 0

                # Validate types
                if not isinstance(price, float):
                    raise ValueError(f"Invalid price value for row {row_num}: {row['price']}")
                if not isinstance(quantity, int):
                    raise ValueError(f"Invalid quantity value for row {row_num}: {row['quantity']}")
                if not isinstance(reorderqty, int):
                    raise ValueError(f"Invalid reorderqty value for row {row_num}: {row['reorderqty']}")

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

        # Process one row at a time to ensure correct type mapping
        total_inserted = 0
        batch_failed_rows = []

        from app.controllers.products import upload_products
        for idx, product_data in enumerate(products_data):
            try:
                result = upload_products(product_data, db)
                total_inserted += result["inserted"]
            except HTTPException as e:
                logger.error(f"Product {idx + 1} failed: {str(e.detail)}")
                batch_failed_rows.append({"product": idx + 1, "error": str(e.detail)})

        response = {
            "message": f"CSV data processed: {total_inserted} products inserted",
            "total_rows": row_count,
            "successful_inserts": total_inserted,
            "failed_rows": failed_rows,
            "batch_errors": batch_failed_rows
        }

        if total_inserted == 0:
            raise HTTPException(status_code=400, detail=response)

        return JSONResponse(status_code=200, content=response)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid data format in CSV: " + str(ve))
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))