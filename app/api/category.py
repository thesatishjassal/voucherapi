from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.category_crud import create_catgeory, get_categories, update_category, delete_category
from app.schema.category import CategoryResponse, CategoryCreate, CategoryUpdate
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
import secrets

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/category/", response_model=CategoryResponse)
async def create_new_category(category: CategoryCreate, db:Session = Depends(get_db_connection)):
        result = create_catgeory(category,db)
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "category added successfully",
            "user": {
                "id": result.id,
                "name": result.catname,
                "slug": result.slug,
            }
        }
    )

@router.get("/category/", response_model=list[CategoryResponse])
async def get_all_categories(db:Session = Depends(get_db_connection)):
    return get_categories(db=db)

@router.put("/category/{category_id}")
async def update_category_api(category_id: int, category_data: CategoryUpdate, db: Session= Depends(get_db_connection)):
    print(category_id)
    try:
        updated_client = update_category(category_data, category_id, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "category updated successfully",
                "client": updated_client
            }
        )
    except HTTPException as e:
        raise e

    
@router.delete("/category/{category_id}")
def delete_category_api(category_id: int, db: Session = Depends(get_db_connection)):
    try:
        result = delete_category(category_id, db)
        return result
    except HTTPException as e:
        raise e

# Include the router in the main app
app.include_router(router)
