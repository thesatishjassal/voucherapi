from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db_connection

from app.schema.arch_register_schema import (
    ArchRegisterSchema
)

from app.controllers.arch_register_controller import (
    create_arch_register_user,
    get_arch_register_users
)

router = APIRouter(
    prefix="/api/arch-register",
    tags=["Arch Register"]
)

# CREATE USER

@router.post("/")
def register_user(
    payload: ArchRegisterSchema,
    db: Session = Depends(get_db_connection)
):

    return create_arch_register_user(
        payload,
        db
    )

# GET USERS

@router.get("/")
def get_users(
    db: Session = Depends(get_db_connection)
):

    return get_arch_register_users(db)