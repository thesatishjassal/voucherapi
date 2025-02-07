from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.user_crud import get_users, create_user, get_user_by_phone, create_login
from app.schema.user_schema import UserResponse
from database import get_db_connection
from app.schema.user_schema import UserCreate, UserResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, HTTPException
import secrets

app = FastAPI()

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db:Session = Depends(get_db_connection)):
    db_user = get_user_by_phone(user.phone, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone Number alredy exist!")
    else:
        result = create_user(user,db)
        session_id = secrets.token_hex(16)
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User added successfully",
            "user": {
                "id": result.id,
                "name": result.name,
                "phone": result.phone,
                "password": result.password
            },
            "session_id": session_id
        }
    )

@router.get("/users/", response_model=list[UserResponse])
async def get_all_users(db:Session = Depends(get_db_connection)):
    return get_users(db=db)

@router.get("/login/")
async def login(db:Session = Depends(get_db_connection)):
    return create_login()

# Include the router in the main app
app.include_router(router)
