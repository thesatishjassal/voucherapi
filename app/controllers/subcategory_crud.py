from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.subcategory import SubCategory
from app.schema.subcategory import SubCategoryCreate
from app.models.user import Base

def create_subcatgeory(subcategory_data: SubCategoryCreate, db: Session):
    subcategory = SubCategory(catname=subcategory_data.catname, subcatname=subcategory_data.subcatname,slug= subcategory_data.slug)
    print(subcategory)
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def get_subcategories(db: Session):
    return db.query(SubCategory).all()
