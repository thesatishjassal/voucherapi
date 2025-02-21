from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.controllers.products import create_products, get_products, delete_product, update_product
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from database import get_db_connection
import shutil
import os

app = FastAPI()
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}




router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.post("/products/{product_id}/upload")
async def upload_product_image(product_id: int, file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed!")

        file_location = f"{UPLOAD_DIR}{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": "Upload successful", "thumbnail": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/products/", response_model=ProductsResponse)
async def create_new_products(products: ProductsCreate, db: Session = Depends(get_db_connection)):
    try:
        result = create_products(products, db)  # This returns a dictionary

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Product added successfully",
                "product": result["product"]  # Accessing the product dictionary
            }
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail["message"], "errors": e.detail["errors"]}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something went wrong", "error": str(e)}
        )

@router.get("/products/", response_model=list[ProductsResponse])
async def get_all_products(db: Session = Depends(get_db_connection)):
    return get_products(db=db)

@router.patch("/products/{product_id}", response_model=ProductsResponse)
def update_product_partial(
    product_id: int, 
    product_data: ProductsUpdate, 
    db: Session = Depends(get_db_connection)
):
    try:
        updated_product = update_product(product_data, product_id, db)
        return {"message": "Product updated successfully", "product": updated_product}
    except HTTPException as e:
        raise e

@router.delete("/products/{product_id}")
def delete_product_api(product_id: int, db: Session = Depends(get_db_connection)):
    try:
        return delete_product(product_id, db)
    except HTTPException as e:
        raise e

app.include_router(router)
