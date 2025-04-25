from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schema.products import ProductsCreate
import csv
import io
from typing import List

def upload_csv(file: UploadFile, db: Session):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = file.file.read()
        csv_file = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)

        products_data: List[ProductsCreate] = []
        for row in csv_reader:
            product_data = ProductsCreate(
                hsncode=row['hsncode'],
                itemcode=row['itemcode'],
                itemname=row['itemname'],
                description=row['description'],
                category=row['category'],
                subcategory=row['subcategory'],
                price=float(row['price']),
                quantity=int(row['quantity']),
                rackcode=row['rackcode'],
                size=row['size'],
                model=row['model'],
                brand=row['brand'],
                unit=row['unit'],
                color=row['color'],
                reorderqty=int(row['reorderqty'])
            )
            products_data.append(product_data)

        # Use your existing upload_products function
        from app.controllers.products import upload_products
        result = upload_products(products_data, db)
        upload_products(products_data, db)
        return JSONResponse(
            status_code=200,
            content={"message": "CSV data uploaded successfully", "records": len(products_data)}
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid data format in CSV: " + str(ve))
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))