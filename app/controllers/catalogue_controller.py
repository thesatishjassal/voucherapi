import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.Catalogue import Catalogue  # Assuming import path; adjust if needed
from app.schema.catalogue import CatalogueCreate, CatalogueUpdate, CatalogueResponse  # Assuming schemas dir

UPLOAD_DIR = "uploads/catalogues"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_URL = "https://api.panvic.in"  # replace with VPS domain or IP

def upload_catalogue_controller(db: Session, name: str, category: str, brand: str, pdf: UploadFile):
    MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB in bytes
    
    # Check file size (pdf.size may be None for streamed uploads; fallback to manual read if needed)
    if pdf.size and pdf.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Max size: 200MB")
    
    # For precise check (if size unavailable), read in chunks:
    # content = await pdf.read()
    # if len(content) > MAX_FILE_SIZE:
    #     raise HTTPException(status_code=413, detail=f"File too large. Max size: 200MB")
    # pdf.file.seek(0)  # Reset for later use
    
    # Validate file type
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Validate file type
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Generate unique filename
    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

    pdf_url = f"/view-catalogue/{filename}"

    # Create DB entry
    catalogue = Catalogue(name=name, category=category or None, brand=brand or None, pdf_url=pdf_url)
    db.add(catalogue)
    db.commit()
    db.refresh(catalogue)

    return {
        "message": "Catalogue uploaded successfully ✅",
        "id": catalogue.id,
        "view_link": f"{BASE_URL}{pdf_url}",
        "download_link": f"{BASE_URL}/download-catalogue/{filename}"
    }

def list_catalogues_controller(db: Session):
    # Query active catalogues (exclude deleted)
    catalogues = db.query(Catalogue).filter(Catalogue.is_deleted == False).order_by(Catalogue.created_at.desc()).all()
    return catalogues

def get_catalogue_controller(db: Session, catalogue_id: int):
    catalogue = db.query(Catalogue).filter(
        and_(Catalogue.id == catalogue_id, Catalogue.is_deleted == False)
    ).first()
    if not catalogue:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    return catalogue

def update_catalogue_controller(
    db: Session, 
    catalogue_id: int, 
    name: str | None, 
    category: str | None, 
    brand: str | None, 
    pdf: UploadFile | None = None
):
    catalogue = db.query(Catalogue).filter(
        and_(Catalogue.id == catalogue_id, Catalogue.is_deleted == False)
    ).first()
    if not catalogue:
        raise HTTPException(status_code=404, detail="Catalogue not found")

    # Update metadata if provided
    if name is not None:
        catalogue.name = name
    if category is not None:
        catalogue.category = category
    if brand is not None:
        catalogue.brand = brand

    # Handle optional PDF update
    if pdf:
        if pdf.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Delete old file
        if catalogue.pdf_url:
            old_filename = catalogue.pdf_url.split("/")[-1]
            old_file_path = os.path.join(UPLOAD_DIR, old_filename)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        # Save new file
        new_filename = f"{uuid.uuid4()}.pdf"
        new_file_path = os.path.join(UPLOAD_DIR, new_filename)
        with open(new_file_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        
        catalogue.pdf_url = f"/view-catalogue/{new_filename}"

    db.commit()
    db.refresh(catalogue)

    return {
        "message": "Catalogue updated successfully ✅",
        "id": catalogue.id,
        "view_link": f"{BASE_URL}{catalogue.pdf_url}" if catalogue.pdf_url else None,
        "download_link": f"{BASE_URL}/download-catalogue/{new_filename}" if pdf else None
    }

def delete_catalogue_controller(db: Session, catalogue_id: int):
    catalogue = db.query(Catalogue).filter(
        and_(Catalogue.id == catalogue_id, Catalogue.is_deleted == False)
    ).first()
    if not catalogue:
        raise HTTPException(status_code=404, detail="Catalogue not found")

    # Hard delete (remove from DB and file)
    if catalogue.pdf_url:
        filename = catalogue.pdf_url.split("/")[-1]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.delete(catalogue)
    db.commit()

    return {"message": "Catalogue deleted successfully ✅", "id": catalogue_id}