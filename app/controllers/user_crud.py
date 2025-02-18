from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate, UserLogin
import bcrypt

def create_user(user_data: UserCreate, db: Session):
    plain_password = user_data.password.encode('utf-8')  # Convert password to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(plain_password, salt)  # Hash the password
    user = User(name=user_data.name, phone=user_data.phone, password=hashed_password)  # Create a user object
    db.add(user)  # Add the user to the session
    db.commit()  # Commit the session to save the user
    db.refresh(user)  # Refresh to load the user with the latest data from the database
    return user

def check_password(plain_text_password: str, hashed_password: str):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')  # Ensure hashed_password is bytes
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

def get_users(db: Session):
    return db.query(User).all()

def create_login(login_data: UserLogin, db: Session):
    user = get_user_by_phone(login_data.phone, db)

    if user:
        # Check if the provided password matches the hashed password in the database
        if check_password(login_data.password, user.password):
            return {
                "message": "Login successful",
                "user_details": {
                    "user_id": user.id,
                    "phone": user.phone,
                    "name": user.name
                }
            }
        else:
            return {"message": "Invalid credentials"}  # More informative error message
    else:
        return {"message": "User not found"}  # More informative error message

def get_user_by_phone(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()
