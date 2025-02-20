from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.subcategory_crud import create_subcatgeory, get_subcategories, delete_subcategory
from app.schema.subcategory import SubCategoryCreate, SubCategoryResponse
from database import get_db_connection
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException
import secrets

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/subcategory/", response_model=SubCategoryResponse)
async def create_new_subcategory(subcategory: SubCategoryCreate, db:Session = Depends(get_db_connection)):
        result = create_subcatgeory(subcategory,db)
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "subcategory added successfully",
            "user": {
                "id": result.id,
                "catname": result.catname,
                "subcatname": result.subcatname,
                "slug": result.slug,
            }
        }
    )

@router.get("/subcategory/", response_model=list[SubCategoryResponse])
async def get_all_subcategories(db:Session = Depends(get_db_connection)):
    return get_subcategories(db=db)

# @router.put("/client/{client_id}")
# def update_client_api(client_id: int, client_data: ClientUpdate, db: Session= Depends(get_db_connection)):
#     print(client_id)
#     try:
#         updated_client= update_client(client_data, client_id, db)
#         return {"message": "Client updated successfully", "client": updated_client}
#     except HTTPException as e:
#         raise e
    
@router.delete("/subcategory/{subcategory_id}")
def delete_subcategory_api(subcategory_id: int, db: Session = Depends(get_db_connection)):
    try:
        result = delete_subcategory(subcategory_id, db)
        return result
    except HTTPException as e:
        raise e

# Include the router in the main app
app.include_router(router)
