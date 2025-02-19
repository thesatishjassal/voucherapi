from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.products import Products
from app.schema.products import ProductsCreate, ProductsResponse, ProductsUpdate
from app.models.user import Base

def create_products(products_data: ProductsCreate, db: Session):
    products = Products(**products_data.model_dump())
    print(products)
    db.add(products)
    db.commit()
    db.refresh(products)
    return products

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