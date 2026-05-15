from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.brand_qr import BrandQR
from app.schema.brand_qr import BrandCreate

import qrcode
import os

QR_FOLDER = "qr_codes"

os.makedirs(QR_FOLDER, exist_ok=True)


# CREATE BRAND
def create_brand_controller(data: BrandCreate, db: Session):

    existing = db.query(BrandQR).filter(
        BrandQR.brand_name == data.brand_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Brand already exists"
        )

    qr = qrcode.make(data.pdf_link)

    file_name = f"{data.brand_name}.png"
    file_path = os.path.join(QR_FOLDER, file_name)

    qr.save(file_path)

    new_brand = BrandQR(
        brand_name=data.brand_name,
        pdf_link=data.pdf_link,
        qr_code=file_path
    )

    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)

    return {
        "message": "Brand created successfully",
        "data": new_brand
    }


# GET ALL BRANDS
def get_all_brands_controller(db: Session):

    brands = db.query(BrandQR).all()

    return brands


# GET BRAND BY NAME
def get_brand_by_name_controller(
    brand_name: str,
    db: Session
):

    brand = db.query(BrandQR).filter(
        BrandQR.brand_name == brand_name
    ).first()

    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    return brand


# UPDATE BRAND
def update_brand_controller(
    id: int,
    data: BrandCreate,
    db: Session
):

    brand = db.query(BrandQR).filter(
        BrandQR.id == id
    ).first()

    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    brand.brand_name = data.brand_name
    brand.pdf_link = data.pdf_link

    qr = qrcode.make(data.pdf_link)

    file_name = f"{data.brand_name}.png"
    file_path = os.path.join(QR_FOLDER, file_name)

    qr.save(file_path)

    brand.qr_code = file_path

    db.commit()

    return {
        "message": "Updated successfully"
    }


# DELETE BRAND
def delete_brand_controller(id: int, db: Session):

    brand = db.query(BrandQR).filter(
        BrandQR.id == id
    ).first()

    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    db.delete(brand)
    db.commit()

    return {
        "message": "Deleted successfully"
    }