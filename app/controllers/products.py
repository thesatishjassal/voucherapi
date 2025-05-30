from http.client import HTTPException
from typing import List, Union
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate
from fastapi import HTTPException
from fastapi import UploadFile
import shutil
import os
import uuid  # For unique file names
from config import UPLOAD_DIR  # Import the correct upload directory
from sqlalchemy import select
import logging

def upload_thumbnail(product_id: int, db: Session, file: UploadFile):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Use JPG, PNG, GIF, or WebP.")

    # Generate unique filename
    file_name = f"product_{product_id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save file to 'uploads' directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store a relative path for frontend access
    public_url = f"/uploads/{file_name}"

    # Update product thumbnail
    product.thumbnail = public_url
    db.commit()
    db.refresh(product)

    return {"message": "Thumbnail uploaded successfully!", "thumbnail": public_url}

def create_products(products_data: ProductsCreate, db: Session):
    # Check for existing product
    existing_product = db.query(Products).filter(
        (Products.hsncode == products_data.hsncode) |
        (Products.itemcode == products_data.itemcode) |
        (Products.itemname == products_data.itemname)
    ).first()

    if existing_product:
        errors = []
        if existing_product.hsncode == products_data.hsncode:
            errors.append("HSN Code already exists.")
        if existing_product.itemcode == products_data.itemcode:
            errors.append("Item Code already exists.")
        if existing_product.itemname == products_data.itemname:
            errors.append("Product Name already exists.")
        raise HTTPException(
            status_code=400,
            detail={"message": "Validation Error", "errors": errors}
        )

    # Create and save the product
    products = Products(**products_data.model_dump())
    db.add(products)
    db.commit()
    db.refresh(products)
    
    return products  # Returns a Products object

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_products(products_data: Union[ProductsCreate, List[ProductsCreate]], db: Session):
    if not isinstance(products_data, list):
        products_data = [products_data]

    inserted_count = 0
    errors = []

    for idx, product_data in enumerate(products_data):
        logger.info(f"Processing product {idx + 1}: hsncode={product_data.hsncode}, itemcode={product_data.itemcode}")

        # Insert as a new product (no unique constraints to worry about)
        product_dict = product_data.model_dump()
        product = Products(**product_dict)
        db.add(product)
        try:
            db.commit()
            db.refresh(product)
            inserted_count += 1
            logger.info(f"Inserted product {idx + 1}: hsncode={product_data.hsncode}, itemcode={product_data.itemcode}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to insert product {idx + 1}: {str(e)}")
            errors.append({"product": product_dict, "error": str(e)})

    if errors:
        raise HTTPException(
            status_code=400,
            detail={"message": "Validation Error", "errors": errors}
        )

    return {"inserted": inserted_count}

def get_products(db: Session):
    return db.query(Products).all()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Products).filter(Products.id == product_id).first()

def update_product(product_data: ProductsUpdate, product_id: int, db: Session):
    product = db.query(Products).filter(Products.id == product_id).first()
    if product:
        # Update the product details with the new data
        if product_data.itemcode:
            product.itemcode = product_data.itemcode
        if product_data.itemname:
            product.itemname = product_data.itemname
        if product_data.hsncode:
            product.hsncode = product_data.hsncode
        if product_data.price:
            product.price = product_data.price
        if product_data.quantity:
            product.quantity = product_data.quantity
        if product_data.rackcode:
            product.rackcode = product_data.rackcode
        if product_data.category:
            product.category = product_data.category
        if product_data.subcategory:
            product.subcategory = product_data.subcategory
        if product_data.size:
            product.size = product_data.size
        if product_data.model:
            product.model = product_data.model
        if product_data.description:
            product.description = product_data.description
        if product_data.unit:
            product.unit = product_data.unit
        # Commit the transaction and refresh the product object to get the updated state
        db.commit()
        db.refresh(product)
        
        return product
    else:
        # If product is not found, raise an exception
        raise HTTPException(status_code=404, detail="Product not found")


def delete_product(product_id: int, db: Session):
    # Find the existing product by ID
    product =  db.query(Products).filter(Products.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"Message" : "product Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="product not found")

def get_product_by_itemcode(itemcode: str, db: Session):
    return db.query(Products).filter(Products.itemcode == itemcode).first()