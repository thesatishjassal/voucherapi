from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers.products import create_products, get_products, update_product, delete_product
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from database import get_db_connection
import shutil
import os

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure uploads directory exists

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Products API"}

@router.post("/products/", response_model=ProductsResponse)
async def create_new_products(products: ProductsCreate, db: Session = Depends(get_db_connection)):
    result = create_products(products, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Product added successfully",
            "product": {
                "id": result.id,
                "itemCode": result.itemCode,
                "itemName": result.itemName,
                "description": result.description,
                "brand": result.brand,
                "hsncode": result.hsncode,
                "category": result.category,
                "subCategory": result.subCategory,
                "size": result.size,
                "model": result.model,
                "price": result.price,
                "quantity": result.quantity,
                "rackCode": result.rackCode,
                # "thumbnail": result.thumbnail,
                "color": result.color
            }
        }
    )

@router.get("/products/", response_model=list[ProductsResponse])
async def get_all_products(db: Session = Depends(get_db_connection)):
    return get_products(db=db)

@router.put("/products/{product_id}")
async def update_product_api(
    product_id: int,
    product_data: ProductsUpdate,
    db: Session = Depends(get_db_connection),
    file: UploadFile = File(None)  # Optional file upload for product image
):
    try:
        # If an image is uploaded, save it
        image_path = None
        if file:
            image_path = f"{UPLOAD_FOLDER}{file.filename}"
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        updated_product = update_product(product_data, product_id, db, image_path)
        
        return {
            "message": "Product updated successfully",
            "product": updated_product
        }
    except HTTPException as e:
        raise e

@router.delete("/products/{product_id}")
async def delete_product_api(product_id: int, db: Session = Depends(get_db_connection)):
    try:
        return delete_product(product_id, db)
    except HTTPException as e:
        raise e
