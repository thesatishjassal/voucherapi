from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schema.category import CategoryCreate, CategoryResponse
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
