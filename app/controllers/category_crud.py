from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schema.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.user import Base

def create_catgeory(category_data: CategoryCreate, db: Session):
    category = Category(name=category_data.name, slug= category_data.slug)
    print(category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.query(Category).all()

def update_category(categorydata: CategoryUpdate, categoryid: int, db: Session):
    category = db.query(Category).filter(categorydata.id == categoryid).first()
    if category:
        # Update the client details with the new data
        if category.name:
            category.name = category.name
        if category.slug:
            category.slug = category.slug
        db.commit()
        db.refresh(category)
        
        return category
    else:
        # If client is not found, raise an exception
        raise HTTPException(status_code=404, detail="Client not found")