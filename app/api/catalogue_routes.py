from fastapi import APIRouter, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.catalogue_controller import (
    upload_catalogue_controller, 
    list_catalogues_controller, 
    get_catalogue_controller,
    update_catalogue_controller,
    delete_catalogue_controller
)
from app.schema.catalogue import CatalogueResponse

router = APIRouter(prefix="/catalogues", tags=["Catalogues"])

@router.post("/upload")
async def upload_catalogue(
    name: str = Form(...),
    category: str = Form(None),
    brand: str = Form(None),
    google_drive_url: str = Form(...),  # New required field
    created_by: str = Form(...),  # New required field
    db: Session = Depends(get_db_connection)
):
    return upload_catalogue_controller(db, name, category, brand, google_drive_url, created_by)

@router.get("/list")
async def list_catalogues(db: Session = Depends(get_db_connection)):
    catalogues = list_catalogues_controller(db)
    return catalogues

@router.get("/list/{catalogue_id}")
async def get_catalogue(catalogue_id: int, db: Session = Depends(get_db_connection)):
    catalogue = get_catalogue_controller(db, catalogue_id)
    return catalogue

@router.put("/{catalogue_id}")
async def update_catalogue(
    catalogue_id: int,
    name: str = Form(None),
    category: str = Form(None),
    brand: str = Form(None),
    google_drive_url: str = Form(None),  # New optional field
    created_by: str = Form(None),  # New optional field
    db: Session = Depends(get_db_connection)
):
    if not any([name, category, brand, google_drive_url, created_by]):
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")
    return update_catalogue_controller(db, catalogue_id, name, category, brand, google_drive_url, created_by)

@router.delete("/{catalogue_id}")
async def delete_catalogue(catalogue_id: int, db: Session = Depends(get_db_connection)):
    return delete_catalogue_controller(db, catalogue_id)

# Removed /view and /download endpoints as no local files; use google_drive_url from responses