from fastapi import (
    APIRouter,
    Depends,
    Body
)

from sqlalchemy.orm import Session

from database import get_db_connection

from app.schema.arch_register_schema import (
    ArchRegisterSchema
)

from app.controllers.arch_register_controller import (
    create_arch_register_user,
    get_arch_register_users,
    approve_architect_user,
    login_user
)

router = APIRouter(
    prefix="/api/arch-register",
    tags=["Arch Register"]
)


# REGISTER USER

@router.post("/")
def register_user(
    payload: ArchRegisterSchema,
    db: Session = Depends(get_db_connection)
):

    return create_arch_register_user(
        payload,
        db
    )


# GET ALL USERS

@router.get("/")
def get_users(
    db: Session = Depends(get_db_connection)
):

    return get_arch_register_users(db)


# APPROVE ARCHITECT

@router.put("/approve/{user_id}")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db_connection)
):

    return approve_architect_user(
        user_id,
        db
    )


# LOGIN USER

@router.post("/login")
def login(
    email: str = Body(...),
    db: Session = Depends(get_db_connection)
):

    return login_user(
        email,
        db
    )