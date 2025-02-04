from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate

def create_user(user_data: UserCreate, db: Session):
    user = User(name=user_data.name, phone= user_data.phone, password=user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()