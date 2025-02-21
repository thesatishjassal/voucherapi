from fastapi import FastAPI
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.products import create_products, get_products, update_product, delete_product
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
                    "color": result.color
                }
            }
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": e.detail["message"],  # Returns "Validation error"
                "errors": e.detail["errors"]     # Returns the list of errors
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something went wrong", "error": str(e)}
        )
    
@router.get("/products/", response_model=list[ProductsResponse])
async def get_all_products(db:Session = Depends(get_db_connection)):
    return get_products(db=db)

@router.put("/products/{product_id}")
def update_product_api(
    product_id: int, 
    product_data: ProductsUpdate, 
    db: Session = Depends(get_db_connection)
):
    print(f"Update Product: {product_id}")  # Improved logging

    try:
        updated_product = update_product(product_data, product_id, db)
        
        return {
            "message": "Product updated successfully", 
            "product": updated_product.__dict__  # Convert SQLAlchemy object to dict
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    
@router.delete("/products/{product_id}")
def delete_product_api(product_id: int, db: Session = Depends(get_db_connection)):
    try:
        result = delete_product(product_id, db)
        return result
    except HTTPException as e:
        raise e

# Include the router in the main app
app.include_router(router)
