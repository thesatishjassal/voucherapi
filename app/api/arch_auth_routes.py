from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schema.arch_auth import ArchLoginRequest
from app.utils.arch_auth_service import arch_login_user
from database import get_db_connection

router = APIRouter(prefix="/api/arch-auth", tags=["Arch Auth"])


@router.post("/login")
def arch_login(
    payload: ArchLoginRequest,
    db: Session = Depends(get_db_connection)
):

    result = arch_login_user(db, payload.email, payload.password)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "success": True,
        "data": result
    }