import random
from datetime import datetime, timedelta

from fastapi import HTTPException

from pymysql import IntegrityError
from sqlalchemy.orm import Session
from app.models.salesperson import SalesPerson

# TODO: point this at whatever module arch-auth already uses to send OTP
# emails, so both flows share one mailer. Until then this is a stand-in
# that you MUST replace before this goes live — it currently does nothing
# but log, so OTPs won't actually reach anyone's inbox.
#
# from app.utils.mailer import send_otp_email
def send_otp_email(email: str, otp: str) -> None:
    print(f"[DEV ONLY] OTP for {email}: {otp}")


OTP_LENGTH = 6
OTP_VALID_MINUTES = 10


class SalesPersonController:

    @staticmethod
    def create(db: Session, payload):
        try:
            salesperson = SalesPerson(**payload.dict())

            db.add(salesperson)
            db.commit()
            db.refresh(salesperson)

            return salesperson

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="A salesperson with this email already exists."
            )

    # ── send OTP (step 1 — and also used for "resend") ──────────────────
    # No password check at all: team login is email + OTP only.

    @staticmethod
    def send_otp(db: Session, payload):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.email == payload.email)
            .first()
        )

        if not salesperson:
            return {
                "success": False,
                "error": "USER_NOT_FOUND",
                "message": "No account found with this email."
            }

        # If you add an approval/status field to the model later, check it
        # here and return ACCOUNT_PENDING_APPROVAL the same way arch-register
        # does, so the frontend's existing handling for that case just works.

        otp = "".join(random.choices("0123456789", k=OTP_LENGTH))

        # NOTE: requires `otp` (String) and `otp_expires_at` (DateTime)
        # columns on the SalesPerson model. Add a migration for these if
        # they don't exist yet:
        #
        #   otp = Column(String(6), nullable=True)
        #   otp_expires_at = Column(DateTime, nullable=True)
        salesperson.otp = otp
        salesperson.otp_expires_at = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
        db.commit()

        send_otp_email(salesperson.email, otp)

        return {
            "success": True,
            "message": "A one-time password has been sent to your email."
        }

    # ── verify OTP (step 2 — completes login) ───────────────────────────

    @staticmethod
    def verify_otp(db: Session, payload):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.email == payload.email)
            .first()
        )

        if not salesperson:
            return {
                "success": False,
                "error": "USER_NOT_FOUND",
                "message": "No account found with this email."
            }

        if not salesperson.otp or not salesperson.otp_expires_at:
            return {
                "success": False,
                "error": "OTP_NOT_REQUESTED",
                "message": "Please request an OTP first."
            }

        if datetime.utcnow() > salesperson.otp_expires_at:
            return {
                "success": False,
                "error": "OTP_EXPIRED",
                "message": "Your OTP has expired. Please request a new one."
            }

        if salesperson.otp != payload.otp:
            return {
                "success": False,
                "error": "INVALID_OTP",
                "message": "Incorrect OTP. Please check and try again."
            }

        # OTP is one-time-use — clear it once consumed.
        salesperson.otp = None
        salesperson.otp_expires_at = None
        db.commit()

        return {
            "success": True,
            "data": {
                "id": salesperson.id,
                "name": salesperson.name,
                "email": salesperson.email,
                "phone": salesperson.phone,
                "architecture_name": salesperson.architecture_name,
                "company_name": salesperson.company_name,
            }
        }

    @staticmethod
    def get_all(db: Session):
        return db.query(SalesPerson).all()

    @staticmethod
    def get_by_id(db: Session, salesperson_id: int):
        return (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

    @staticmethod
    def update(db: Session, salesperson_id: int, payload):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return None

        update_data = payload.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(salesperson, key, value)

        db.commit()
        db.refresh(salesperson)

        return salesperson

    @staticmethod
    def delete(db: Session, salesperson_id: int):
        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return False

        db.delete(salesperson)
        db.commit()

        return True