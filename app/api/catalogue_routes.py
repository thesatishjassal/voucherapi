from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.catalogue_controller import (
    upload_catalogue_controller, 
    list_catalogues_controller, 
    get_catalogue_controller,
    update_catalogue_controller,
    delete_catalogue_controller
)
from app.schema.catalogue import CatalogueResponse  # Assuming schemas dir
import os

router = APIRouter(prefix="/catalogues", tags=["Catalogues"])

UPLOAD_DIR = "uploads/catalogues"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_catalogue(
    name: str = Form(...),
    category: str = Form(None),  # Optional now
    brand: str = Form(None),     # Optional now
    pdf: UploadFile = File(...),
    db: Session = Depends(get_db_connection)
):
    return upload_catalogue_controller(db, name, category, brand, pdf)

@router.get("/list")
async def list_catalogues(db: Session = Depends(get_db_connection)):
    catalogues = list_catalogues_controller(db)
    return catalogues  # Auto-serializes to CatalogueResponse via orm_mode

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
    pdf: UploadFile = File(None),  # Optional file
    db: Session = Depends(get_db_connection)
):
    if not any([name, category, brand, pdf]):  # Require at least one field
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")
    return update_catalogue_controller(db, catalogue_id, name, category, brand, pdf)

@router.delete("/{catalogue_id}")
async def delete_catalogue(catalogue_id: int, db: Session = Depends(get_db_connection)):
    return delete_catalogue_controller(db, catalogue_id)

@router.get("/view/{filename}")
async def view_catalogue(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Catalogue not found")
    return FileResponse(file_path, media_type="application/pdf")

@router.get("/download/{filename}")
async def download_catalogue(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Catalogue not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)