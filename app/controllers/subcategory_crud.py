from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.subcategory import SubCategory
from app.schema.subcategory import SubCategoryCreate, SubCategoryUpdate
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

def update_subcategory(subcategorydata: SubCategoryUpdate, subcategoryid: int, db: Session):
    subcategory = db.query(SubCategory).filter(subcategorydata.id == subcategoryid).first()
    if subcategory:
        # Update the client details with the new data
        if subcategory.subcatname:
            subcategory.subcat = subcategory.subcat
        if subcategory.catname:
            subcategory.catname = subcategory.catname
        if subcategory.slug:
            subcategory.slug = subcategory.slug
        db.commit()
        db.refresh(subcategory)
        
        return subcategory
    else:
        # If client is not found, raise an exception
        raise HTTPException(status_code=404, detail="Client not found")
    
def delete_subcategory(subcategory_id: int, db: Session):
    # Find the existing client by ID
    subcategory =  db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if subcategory:
        db.delete(subcategory)
        db.commit()
        return {"Message" : "Subcategory Deleted Successfuly!"}
    else:
        raise HTTPException(status_code=404, detail="Subcategory not found")
