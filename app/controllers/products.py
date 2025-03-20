from http.client import HTTPException
from typing import List, Union
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate
from fastapi import HTTPException
from fastapi import UploadFile, File
# from sqlalchemy.orm import Session
# from app.models.products import Products
import shutil
import os
import uuid  # For unique file names
from config import UPLOAD_DIR  # Import the correct upload directory

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

def upload_products(products_data: Union[ProductsCreate, List[ProductsCreate]], db: Session):

    # Ensure products_data is a list for uniform processing
    if not isinstance(products_data, list):
        products_data = [products_data]

    created_products = []
    errors = []

    for product_data in products_data:
        # Check for existing product conflicts
        existing_product = db.query(Products).filter(
            (Products.hsncode == product_data.hsncode) |
            (Products.itemcode == product_data.itemcode) |
            (Products.itemname == product_data.itemname)
        ).first()

        if existing_product:
            product_errors = {"itemcode": product_data.itemcode, "errors": []}
            if existing_product.hsncode == product_data.hsncode:
                product_errors["errors"].append("HSN Code already exists.")
            if existing_product.itemcode == product_data.itemcode:
                product_errors["errors"].append("Item Code already exists.")
            if existing_product.itemname == product_data.itemname:
                product_errors["errors"].append("Product Name already exists.")
            errors.append(product_errors)
            continue  # Skip adding this product and move to next

        # Create and append product if no conflicts
        product = Products(**product_data.model_dump())
        db.add(product)
        created_products.append(product)

    if errors:
        # If any errors occurred, raise exception without committing anything
        raise HTTPException(
            status_code=400,
            detail={"message": "Validation Error", "errors": errors}
        )

    # Commit only if all products are valid and added
    db.commit()

    # Refresh all created products to get DB-generated fields like IDs
    for product in created_products:
        db.refresh(product)

    # Return single product if only one was added, otherwise return the list
    return created_products[0] if len(created_products) == 1 else created_products


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
            product.itemname = product_data.subcategory
        if product_data.size:
            product.size = product_data.size
        if product_data.model:
            product.model = product_data.model
        if product_data.description:
            product.description = product_data.model
        if product_data.unit:
            product.unit = product_data.model
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