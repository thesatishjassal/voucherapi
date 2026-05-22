from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database import get_db_connection

from app.utils.arch_auth_service import (
    send_otp,
    verify_user_otp
)

router = APIRouter(
    prefix="/api/arch-auth",
    tags=["Arch OTP Auth"]
)

# -------------------------
# SCHEMAS
# -------------------------

class SendOtpSchema(BaseModel):
    email: EmailStr


class VerifyOtpSchema(BaseModel):
    email: EmailStr
    otp: str


# -------------------------
# SEND OTP
# -------------------------

@router.post("/send-otp")
def send_otp_api(
    payload: SendOtpSchema,
    db: Session = Depends(get_db_connection)
):

    send_otp(db, payload.email)

    return {
        "success": True,
        "message": "OTP sent successfully"
    }


# -------------------------
# VERIFY OTP
# -------------------------

@router.post("/verify-otp")
def verify_otp_api(
    payload: VerifyOtpSchema,
    db: Session = Depends(get_db_connection)
):

    ok = verify_user_otp(
        db,
        payload.email,
        payload.otp
    )

    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    return {
        "success": True,
        "message": "User verified successfully"
    }