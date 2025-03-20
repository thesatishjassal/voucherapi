from fastapi import FastAPI, File, UploadFile
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.products import get_product_by_id, create_products, get_products, update_product, delete_product, upload_thumbnail
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException
import secrets

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

from fastapi import HTTPException

@router.post("/products/", response_model=ProductsResponse)
async def create_new_products(products: ProductsCreate, db: Session = Depends(get_db_connection)):
    try:
        result = create_products(products, db)

        # Convert result to a dictionary, only including serializable fields
        product_dict = {key: getattr(result, key) for key in ProductsResponse.__annotations__ if hasattr(result, key)}
        
        # Add success message separately
        return {**product_dict, "message": "Product added successfully"}
    
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Something went wrong", "error": str(e)}
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
