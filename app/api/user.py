from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.controllers.user_crud import get_users, create_user, get_user_by_phone
from app.schema.user_schema import UserResponse
from database import get_db_connection
from app.schema.user_schema import UserCreate, UserResponse
from fastapi.responses import JSONResponse

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
        return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": f"User added successfully, {result}"}
    )

@router.get("/users/", response_model=list[UserResponse])
async def get_all_users(db:Session = Depends(get_db_connection)):
    return get_users(db=db)

# Include the router in the main app
app.include_router(router)
