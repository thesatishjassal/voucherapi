from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schema.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.user import Base

def create_catgeory(category_data: CategoryCreate, db: Session):
    category = Category(catname=category_data.catname, slug= category_data.slug)
    print(category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.query(Category).all()

def update_category(categorydata: CategoryUpdate, categoryid: int, db: Session):
    category = db.query(Category).filter(Category.id == categoryid).first()
    print(categoryid)
    if category:
        # Update the client details with the new data
        if categorydata.catname:
            category.catname = categorydata.catname
        if categorydata.slug:
            category.slug = categorydata.slug
        db.commit()
        db.refresh(category)
        
        return category
    else:
        # If client is not found, raise an exception
        raise HTTPException(status_code=404, detail="Client not found")
    
def delete_category(category_id: int, db: Session):
    # Find the existing client by ID
    category =  db.query(Category).filter(Category.id ==category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return {"Message" : "category Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")
