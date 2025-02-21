import os
from fastapi import HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate
from database import get_db_connection

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

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
            detail={"message": "Validation Error", "errors": errors}
        )

    # Create and save the product
    products = Products(**products_data.model_dump())
    db.add(products)
    db.commit()
    db.refresh(products)

    return {"message": "Product created successfully!", "product": products}

def get_products(db: Session):
    return db.query(Products).all()

def update_product(product_data: ProductsUpdate, product_id: int, db: Session):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_fields = [
        "hsncode", "itemCode", "itemName", "description", "category", "subCategory",
        "price", "quantity", "rackCode", "size", "color", "model", "brand"
    ]

    for field in update_fields:
        value = getattr(product_data, field)
        if value is not None:
            setattr(product, field, value)

    if product_data.thumbnail:
        product.thumbnail = product_data.thumbnail  # URL or path

    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    product = db.query(Products).filter(Products.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Remove the image file
    if product.thumbnail:
        try:
            os.remove(product.thumbnail)
        except FileNotFoundError:
            pass

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully!"}

def get_product_by_itemcode(itemcode: str, db: Session):
    return db.query(Products).filter(Products.itemCode == itemcode).first()

# ✅ New Function: Upload Image
def upload_product_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db_connection)):
    product = db.query(Products).filter(Products.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    file_extension = os.path.splitext(file.filename)[-1]
    filename = f"product_{product_id}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    product.thumbnail = file_path  # Save path in the database
    db.commit()
    db.refresh(product)

    return {"message": "Image uploaded successfully", "image_url": file_path}
