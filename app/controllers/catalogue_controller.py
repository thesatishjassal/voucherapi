import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.Catalogue import Catalogue  # Adjust import if needed

BASE_URL = "https://api.panvic.in"  # For API consistency, though not used for Drive links

def upload_catalogue_controller(db: Session, name: str, category: str, brand: str, google_drive_url: str, created_by: str):
    # Basic validation for URL (simple check; enhance if needed)
    if not google_drive_url.startswith("https://drive.google.com"):
        raise HTTPException(status_code=400, detail="Invalid Google Drive URL. Must start with https://drive.google.com")

    # Create DB entry
    catalogue = Catalogue(
        name=name, 
        category=category or None, 
        brand=brand or None, 
        google_drive_url=google_drive_url,
        created_by=created_by
    )
    db.add(catalogue)
    db.commit()
    db.refresh(catalogue)

    return {
        "message": "Catalogue created successfully ✅",
        "id": catalogue.id,
        "google_drive_link": google_drive_url  # Single link for view/download
    }

def list_catalogues_controller(db: Session):
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
    google_drive_url: str | None, 
    created_by: str | None
):
    catalogue = db.query(Catalogue).filter(
        and_(Catalogue.id == catalogue_id, Catalogue.is_deleted == False)
    ).first()
    if not catalogue:
        raise HTTPException(status_code=404, detail="Catalogue not found")

    # Update fields if provided
    if name is not None:
        catalogue.name = name
    if category is not None:
        catalogue.category = category
    if brand is not None:
        catalogue.brand = brand
    if google_drive_url is not None:
        if not google_drive_url.startswith("https://drive.google.com"):
            raise HTTPException(status_code=400, detail="Invalid Google Drive URL")
        catalogue.google_drive_url = google_drive_url
    if created_by is not None:
        catalogue.created_by = created_by

    db.commit()
    db.refresh(catalogue)

    return {
        "message": "Catalogue updated successfully ✅",
        "id": catalogue.id,
        "google_drive_link": catalogue.google_drive_url
    }

def delete_catalogue_controller(db: Session, catalogue_id: int):
    catalogue = db.query(Catalogue).filter(
        and_(Catalogue.id == catalogue_id, Catalogue.is_deleted == False)
    ).first()
    if not catalogue:
        raise HTTPException(status_code=404, detail="Catalogue not found")

    # Hard delete (no file to remove)
    db.delete(catalogue)
    db.commit()

    return {"message": "Catalogue deleted successfully ✅", "id": catalogue_id}