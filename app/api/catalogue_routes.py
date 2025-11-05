from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db_connection
from app.controllers.catalogue_controller import upload_catalogue_controller, list_catalogues_controller
import os

router = APIRouter(prefix="/catalogues", tags=["Catalogues"])

UPLOAD_DIR = "uploads/catalogues"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_catalogue(
    name: str = Form(...),
    category: str = Form(...),
    brand: str = Form(...),
    pdf: UploadFile = File(...),
    db: Session = Depends(get_db_connection)
):
    return upload_catalogue_controller(db, name, category, brand, pdf)

@router.get("/list")
async def list_catalogues(db: Session = Depends(get_db_connection)):
    return list_catalogues_controller(db)

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
