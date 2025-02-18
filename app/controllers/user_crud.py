from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate, UserLogin

def create_user(user_data: UserCreate, db: Session):
    # Directly store the plain password without hashing
    user = User(name=user_data.name, phone=user_data.phone, password=user_data.password)  # Store plain password
    db.add(user)  # Add the user to the session
    db.commit()  # Commit the session to save the user
    db.refresh(user)  # Refresh to load the user with the latest data from the database
    return user

def check_password(plain_text_password: str, stored_password: str):
    # Directly compare the plain text password with the stored password
    return plain_text_password == stored_password

def get_users(db: Session):
    return db.query(User).all()

def create_login(login_data: UserLogin, db: Session):
    user = get_user_by_phone(login_data.phone, db)

    if user:
        # Check if the provided password matches the stored hashed password
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
            return {"message": "Invalid credentials"}  # Incorrect password
    
    else:
        return {"message": "User not found"}  # User does not exist

def get_user_by_phone(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()
