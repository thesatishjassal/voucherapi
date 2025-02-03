from fastapi import FastAPI, APIRouter, HTTPException
from app.models import user
from app.crud.user_crud import get_users, create_users
from app.schemas.user_schema import UserResponse

app = FastAPI()
# Root route - move it to the main app

@app.get("/")
def read_root():
    return {"Hello": "World"}

router = APIRouter()

@router.post("/users/")
async def create_new_user(user: user.User):
    result =  create_users(user)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/users/", response_model=UserResponse)
async def get_all_users():
    users = get_users()
    if not users:
        raise HTTPException(status_code=404, detail="Users Not Found!")
    return {"users" : users}
    

# app.include_router(router, prefix="/api")