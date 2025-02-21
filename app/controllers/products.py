from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate

# from fastapi import HTTPException
from fastapi import UploadFile, File
# from sqlalchemy.orm import Session
# from app.models.products import Products
import shutil
import os
import uuid  # For unique file names

UPLOAD_DIR = "uploads/"  # Define the upload directory
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists


def upload_thumbnail(product_id: int, db: Session, file: UploadFile = File(...)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Extract file extension (e.g., .jpg, .png)
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Use JPG, PNG, GIF, or WebP.")

    # Generate a unique filename
    file_name = f"product_{product_id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the product thumbnail
    product.thumbnail = file_path
    db.commit()
    db.refresh(product)

    return {"message": "Thumbnail uploaded successfully!", "thumbnail": file_path}

def create_products(products_data: ProductsCreate, db: Session):
    # Check for existing product
    existing_product = db.query(Products).filter(
        (Products.hsncode == products_data.hsncode) |
        (Products.itemCode == products_data.itemCode) |
        (Products.itemName == products_data.itemName)
    ).first()

    if existing_product:
        errors = []
        if existing_product.hsncode == products_data.hsncode:
            errors.append("HSN Code already exists.")
        if existing_product.itemCode == products_data.itemCode:
            errors.append("Item Code already exists.")
        if existing_product.itemName == products_data.itemName:
            errors.append("Product Name already exists.")

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Validation Error",
                "errors": errors
            }
        )

    # Create and save the product
    products = Products(**products_data.model_dump())
    db.add(products)
    db.commit()
    db.refresh(products)

    return {
        "message": "Product created successfully!",
        "product": products
    }


def get_products(db: Session):
    return db.query(Products).all()

def update_product(product_data: ProductsUpdate, product_id: int, db: Session):
    product = db.query(Products).filter(Products.id == product_id).first()
    if product:
        # Update the product details with the new data
        if product_data.itemCode:
            product.itemCode = product_data.itemCode
        if product_data.itemName:
            product.itemName = product_data.itemName
        if product_data.hsncode:
            product.hsncode = product_data.hsncode
        if product_data.price:
            product.price = product_data.price
        if product_data.quantity:
            product.quantity = product_data.quantity
        if product_data.rackCode:
            product.rackCode = product_data.rackCode
        if product_data.category:
            product.category = product_data.category
        if product_data.subCategory:
            product.subCategory = product_data.subCategory
        if product_data.size:
            product.size = product_data.size
        if product_data.model:
            product.model = product_data.model
        if product_data.description:
            product.description = product_data.model
        # Commit the transaction and refresh the product object to get the updated state
        db.commit()
        db.refresh(product)
        
        return product
    else:
        # If product is not found, raise an exception
        raise HTTPException(status_code=404, detail="Product not found")


def delete_product(product_id: int, db: Session):
    # Find the existing product by ID
    product =  db.query(Products).filter(product_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"Message" : "product Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="product not found")

def get_product_by_itemcode(itemcode: str, db: Session):
    return db.query(Products).filter(Products.itemCode == itemcode).first()