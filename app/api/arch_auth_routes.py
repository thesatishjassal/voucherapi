from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection
from app.utils.arch_auth_service import send_otp, verify_user_otp

router = APIRouter(prefix="/api/arch-auth", tags=["Arch OTP Auth"])


# 📩 SEND OTP
@router.post("/send-otp")
def send_otp_api(email: str, db: Session = Depends(get_db_connection)):

    send_otp(db, email)

    return {
        "success": True,
        "message": "OTP sent successfully"
    }


# 🔐 VERIFY OTP
@router.post("/verify-otp")
def verify_otp_api(
    email: str,
    otp: str,
    db: Session = Depends(get_db_connection)
):

    ok = verify_user_otp(db, email, otp)

    if not ok:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    return {
        "success": True,
        "message": "User verified successfully"
    }