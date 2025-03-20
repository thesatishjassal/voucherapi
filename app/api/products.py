from fastapi import FastAPI, File, UploadFile
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.products import get_product_by_id, create_products, get_products, update_product, delete_product, upload_thumbnail
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException
import secrets
from app.models.products import Products

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

from fastapi import HTTPException

@router.post("/products/", response_model=ProductsResponse)
async def create_new_product(product: ProductsCreate, db: Session = Depends(get_db_connection)):
    # Check for existing product
    existing_product = db.query(Products).filter(
        (Products.hsncode == product.hsncode) |
        (Products.itemcode == product.itemcode) |
        (Products.itemname == product.itemname)
    ).first()

    if existing_product:
        errors = []
        if existing_product.hsncode == product.hsncode:
            errors.append("HSN Code already exists.")
        if existing_product.itemcode == product.itemcode:
            errors.append("Item Code already exists.")
        if existing_product.itemname == product.itemname:
            errors.append("Product Name already exists.")

        raise HTTPException(status_code=400, detail={"message": "Validation Error", "errors": errors})

    # Create new product
    result = create_products(product, db)
    session_id = secrets.token_hex(16)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Product added successfully",
            "product": {
                "id": result.id,
                "hsncode": result.hsncode,
                "itemcode": result.itemcode,
                "itemname": result.itemname,
                "description": result.description,
                "category": result.category,
                "subcategory": result.subcategory,
                "price": result.price,
                "quantity": result.quantity,
                "rackcode": result.rackcode,
                "thumbnail": result.thumbnail,
                "size": result.size,
                "color": result.color,
                "model": result.model,
                "brand": result.brand,
                "unit": result.unit
            },
            "session_id": session_id
        }
    )
    
@router.get("/products/", response_model=list[ProductsResponse])
async def get_all_products(db:Session = Depends(get_db_connection)):
    return get_products(db=db)

@router.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db_connection)):
    product = get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}")
def update_product_api(product_id: str, product_data: ProductsUpdate, db: Session= Depends(get_db_connection)):
    print("Update Product", {product_id})
    try:
        updated_product=update_product(product_data, product_id, db)
        return {"message": "Product updated successfully", "Product":  updated_product}
    except HTTPException as e:
        raise e
    
@router.delete("/products/{product_id}")
def delete_product_api(product_id: str, db: Session = Depends(get_db_connection)):
    try:
        result = delete_product(product_id, db)
        return result
    except HTTPException as e:
        raise e

# ✅ **New Thumbnail Upload Endpostr**
@router.post("/products/{product_id}/upload/")
async def upload_product_thumbnail(
    product_id: str,
    file: UploadFile = File(...),  # ✅ Ensure `File(...)` is present
    db: Session = Depends(get_db_connection)
):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    print(f"Received file: {file.filename}")  # Debugging Line

    try:
        result = upload_thumbnail(product_id, db, file)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Thumbnail upload failed", "error": str(e)}
        )

            
# Include the router in the main app
app.include_router(router)
