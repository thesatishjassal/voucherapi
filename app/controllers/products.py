from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Products  # Assuming you have a Products model

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

        raise HTTPException(status_code=400, detail={"message": "Validation error", "errors": errors})

    # Create and save the product
    products = Products(**products_data.model_dump())
    db.add(products)
    db.commit()
    db.refresh(products)
    return products


def get_products(db: Session):
    return db.query(Products).all()

def update_product(product_data: ProductsUpdate, product_id: int, db: Session, image_path=None):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product details
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
        product.description = product_data.description

    # Update image if provided
    if image_path:
        product.thumbnail = image_path

    db.commit()
    db.refresh(product)
    
    return product

def delete_product(product_id: int, db: Session):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    
    return {"message": "Product deleted successfully!"}
