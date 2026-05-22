from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.arch_user import ArchUser
from app.models.arch_otp import ArchOtp

from app.utils.arch_security import (
    generate_otp,
    hash_otp,
    verify_otp
)

# -------------------------
# SEND OTP
# -------------------------
def send_otp(
    db: Session,
    email: str
):

    # generate otp
    otp = generate_otp()

    # hash otp
    otp_hash = hash_otp(otp)

    # expiry
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # save otp
    otp_record = ArchOtp(
        email=email,
        otp_hash=otp_hash,
        expires_at=expires_at
    )

    db.add(otp_record)
    db.commit()

    # create user if not exists
    user = (
        db.query(ArchUser)
        .filter(ArchUser.email == email)
        .first()
    )

    if not user:

        user = ArchUser(
            email=email,
            is_verified=False
        )

        db.add(user)
        db.commit()

    # temporary debug otp
    print(f"OTP for {email}: {otp}")

    return {
        "success": True,
        "message": "OTP sent successfully"
    }

# -------------------------
# VERIFY OTP
# -------------------------
def verify_user_otp(
    db: Session,
    email: str,
    otp: str
):

    otp_record = (
        db.query(ArchOtp)
        .filter(ArchOtp.email == email)
        .order_by(ArchOtp.id.desc())
        .first()
    )

    if not otp_record:
        return False

    # check expiry
    if otp_record.expires_at < datetime.utcnow():
        return False

    # verify otp
    is_valid = verify_otp(
        otp,
        otp_record.otp_hash
    )

    if not is_valid:
        return False

    # verify user
    user = (
        db.query(ArchUser)
        .filter(ArchUser.email == email)
        .first()
    )

    if user:
        user.is_verified = True
        db.commit()

    return True