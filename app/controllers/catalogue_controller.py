import os, shutil, uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.Catalogue import Catalogue

UPLOAD_DIR = "uploads/catalogues"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_URL = "https://api.panvic.in"  # replace with VPS domain or IP

def upload_catalogue_controller(db: Session, name: str, category: str, brand: str, pdf: UploadFile):
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
    catalogue = Catalogue(name=name, category=category, brand=brand, pdf_url=pdf_url)
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
    return db.query(Catalogue).order_by(Catalogue.created_at.desc()).all()
