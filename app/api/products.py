from fastapi import FastAPI
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.products import create_products, get_products, delete_product
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from app.models.products import Products

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

@router.patch("/products/{product_id}", response_model=ProductsResponse)
def update_product_partial(
    product_id: int, 
    product_data: ProductsUpdate,  # ✅ Use Pydantic model instead of dict
    db: Session = Depends(get_db_connection)
):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # ✅ Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)  # Ignore unset fields
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {"message": "Product updated successfully", "product": product}
    
@router.delete("/products/{product_id}")
def delete_product_api(product_id: int, db: Session = Depends(get_db_connection)):
    try:
        result = delete_product(product_id, db)
        return result
    except HTTPException as e:
        raise e

# Include the router in the main app
app.include_router(router)
