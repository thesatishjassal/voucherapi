from typing import List
from fastapi import FastAPI, APIRouter, HTTPException
from app.models import user
from app.controllers.user_crud import get_users, create_users
from app.models.user import UserResponse

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/users/")
async def create_new_user(user: user.User):
    # Call the function to create a user
    result = create_users(user)
    
    # Handle cases where no result is returned, indicating a failure
    if result is None:
        raise HTTPException(status_code=400, detail="Error creating user")
    
    # Return a success message with the inserted user data
    return {"message": "User created successfully", "data": result}

@router.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    # Get all users from the database
    users = get_users()
    
    # Handle the case when no users are found
    if not users:
        raise HTTPException(status_code=404, detail="Users Not Found!")
    
    # Return the list of users
    return users

# Include the router in the main app
app.include_router(router)
