from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsUpdate

from fastapi import HTTPException

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

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only the provided fields
    update_fields = [
        "hsncode", "itemCode", "itemName", "description", "category", "subCategory",
        "price", "quantity", "rackCode", "size", "color", "model", "brand"
    ]

    for field in update_fields:
        value = getattr(product_data, field)
        if value is not None:
            setattr(product, field, value)

    # ✅ Handle thumbnail update separately (if provided)
    if product_data.thumbnail:
        product.thumbnail = product_data.thumbnail  # Can be Base64 or URL
    
    # Commit the changes
    db.commit()
    db.refresh(product)

    return product


def delete_product(product_id: int, db: Session):
    # Corrected filter condition
    product = db.query(Products).filter(Products.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully!"}

def get_product_by_itemcode(itemcode: str, db: Session):
    return db.query(Products).filter(Products.itemCode == itemcode).first()