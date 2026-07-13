import random
from datetime import datetime, timedelta

from fastapi import HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from app.models.salesperson import SalesPerson

# Replace this with your actual email sender
def send_otp_email(email: str, otp: str):
    print(f"[DEV] OTP for {email}: {otp}")


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
                detail={
                    "email": "This email is already registered."
                }
            )

    # --------------------------------------------------------
    # Send OTP
    # --------------------------------------------------------

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

        otp = "".join(
            random.choices(
                "0123456789",
                k=OTP_LENGTH
            )
        )

        salesperson.otp = otp
        salesperson.otp_expires_at = (
            datetime.utcnow() +
            timedelta(minutes=OTP_VALID_MINUTES)
        )

        db.commit()

        send_otp_email(
            salesperson.email,
            otp
        )

        return {
            "success": True,
            "message": "OTP sent successfully."
        }

    # --------------------------------------------------------
    # Verify OTP
    # --------------------------------------------------------

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

        if not salesperson.otp:
            return {
                "success": False,
                "error": "OTP_NOT_REQUESTED",
                "message": "Please request an OTP first."
            }

        if salesperson.otp_expires_at < datetime.utcnow():
            return {
                "success": False,
                "error": "OTP_EXPIRED",
                "message": "OTP has expired."
            }

        if salesperson.otp != payload.otp:
            return {
                "success": False,
                "error": "INVALID_OTP",
                "message": "Invalid OTP."
            }

        salesperson.otp = None
        salesperson.otp_expires_at = None

        db.commit()

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "id": salesperson.id,
                "name": salesperson.name,
                "email": salesperson.email,
                "phone": salesperson.phone,
                "architecture_name": salesperson.architecture_name,
                "company_name": salesperson.company_name,
            }
        }

    # --------------------------------------------------------
    # Get All
    # --------------------------------------------------------

    @staticmethod
    def get_all(db: Session):
        return db.query(SalesPerson).all()

    # --------------------------------------------------------
    # Get By ID
    # --------------------------------------------------------

    @staticmethod
    def get_by_id(db: Session, salesperson_id: int):

        return (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

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