from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.arch_user import ArchUser
from app.models.arch_otp import ArchOtp
from app.utils.arch_auth_service import generate_otp, hash_otp, verify_otp


def send_otp(db: Session, email: str):
    otp = generate_otp()
    otp_hash = hash_otp(otp)

    expires = datetime.utcnow() + timedelta(minutes=5)

    db.add(ArchOtp(
        email=email,
        otp_hash=otp_hash,
        expires_at=expires
    ))

    db.commit()

    # 🔥 HERE: integrate email/SMS service
    print(f"OTP for {email}: {otp}")

    return True


def verify_user_otp(db: Session, email: str, otp: str):
    record = db.query(ArchOtp).filter(
        ArchOtp.email == email
    ).order_by(ArchOtp.id.desc()).first()

    if not record:
        return False

    if record.expires_at < datetime.utcnow():
        return False

    if not verify_otp(otp, record.otp_hash):
        return False

    user = db.query(ArchUser).filter(ArchUser.email == email).first()
    if user:
        user.is_verified = True

    db.commit()

    return True