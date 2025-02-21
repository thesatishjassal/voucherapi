from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from sqlalchemy.orm import Session
from database import get_db_connection  # Import database session
from app.models.products import Products  # Import the Product model

app = FastAPI()

# Allowed origins for CORS
origins = [
    "http://localhost:3000",
    "https://www.panvik.in",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@app.post("/products/{product_id}/upload")
async def upload_product_image(
    product_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db_connection)
):
    """
    Uploads an image for a product by its ID and updates the 'thumbnail' field.
    """
    try:
        # Ensure file is an image
        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

        # Create product folder
        product_folder = os.path.join(UPLOAD_DIR, str(product_id))
        Path(product_folder).mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = os.path.join(product_folder, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Update database (assuming `Product` model has `thumbnail` field)
        product = db.query(Products).filter(Products.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.thumbnail = file_path  # Store the file path in DB
        db.commit()
        db.refresh(product)

        return {"message": "File uploaded successfully", "thumbnail": product.thumbnail}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

