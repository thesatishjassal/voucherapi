from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate, UserLogin
from app.models.user import Base
import bcrypt

def create_user(user_data: UserCreate, db: Session):
    plain_password = user_data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password, salt)
    user = User(name=user_data.name, phone=user_data.phone, password=hashed_password)
    print(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def check_password(plain_text_password: str, hashed_password: str):
    """Ensure hashed_password is bytes before checking"""
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')  # Convert string to bytes
    
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

def get_users(db: Session):
    return db.query(User).all()

def create_login(login_data: UserCreate,  db: Session):
    user = get_user_by_phone(login_data.phone, db)
    if user:
        if check_password(login_data.password, user.password):
            return "Logged In"
        else:
            return "Invalid credentials"
    else:
        return "User not found"

def get_user_by_phone(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()
