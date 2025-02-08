from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Login, User
from app.schema.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user import Base
import bcrypt

def create_user(user_data: UserCreate, db: Session):
    plain_password = user_data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password, salt)
    user = User(name=user_data.name, phone= user_data.phone, password=hashed_password)
    print(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Verify the password
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

def get_users(db: Session):
    return db.query(User).all()

def create_login(user_data: UserLogin, db: Session):
    user = Login(phone= user_data.phone, password=user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()