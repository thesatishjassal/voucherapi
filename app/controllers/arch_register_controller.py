from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.arch_register_model import (
    ArchRegister
)

ALLOWED_ROLES = [
    "admin",
    "architect",
    "sales_person"
]


# REGISTER USER

def create_arch_register_user(
    payload,
    db: Session
):

    existing_user = (
        db.query(ArchRegister)
        .filter(
            ArchRegister.email == payload.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # VALIDATE ROLE

    if payload.role not in ALLOWED_ROLES:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    # APPROVAL LOGIC

    is_approved = True

    # Architect needs approval

    if payload.role == "architect":

        is_approved = False

    user = ArchRegister(

        # AUTH

        role=payload.role,
        is_approved=is_approved,

        # STEP 1

        full_name=payload.full_name,
        firm_name=payload.firm_name,
        mobile_number=payload.mobile_number,
        email=payload.email,
        date_of_birth=payload.date_of_birth,
        profession=payload.profession,
        marital_status=payload.marital_status,
        anniversary_date=payload.anniversary_date,

        # STEP 2

        account_holder_name=payload.account_holder_name,
        bank_name=payload.bank_name,
        account_number=payload.account_number,
        ifsc_code=payload.ifsc_code,
        upi_id=payload.upi_id,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    # ARCHITECT RESPONSE

    if user.role == "architect":

        return {
            "success": True,
            "message": "Registration successful. Wait for admin approval.",
            "session_created": False,
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
                "is_approved": user.is_approved
            }
        }

    # ADMIN + SALES PERSON RESPONSE

    return {
        "success": True,
        "message": "Registration successful",
        "session_created": True,
        "data": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_approved": user.is_approved
        }
    }


# GET ALL USERS

def get_arch_register_users(
    db: Session
):

    users = db.query(ArchRegister).all()

    return {
        "success": True,
        "count": len(users),
        "data": users
    }


# APPROVE ARCHITECT

def approve_architect_user(
    user_id: int,
    db: Session
):

    user = (
        db.query(ArchRegister)
        .filter(
            ArchRegister.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_approved = True

    db.commit()

    db.refresh(user)

    return {
        "success": True,
        "message": "Architect approved successfully",
        "data": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_approved": user.is_approved
        }
    }


# LOGIN USER

def login_user(
    email: str,
    db: Session
):

    user = (
        db.query(ArchRegister)
        .filter(
            ArchRegister.email == email
        )
        .first()
    )

    # USER NOT FOUND

    if not user:

        return {
            "success": False,
            "status_code": 404,
            "message": "Account not found.",
            "error": "USER_NOT_FOUND",
            "data": None
        }

    # ARCHITECT NOT APPROVED

    if (
        user.role == "architect"
        and
        not user.is_approved
    ):

        return {
            "success": False,
            "status_code": 403,
            "message": "Your account is pending admin approval. Please wait until your registration is reviewed.",
            "error": "ACCOUNT_PENDING_APPROVAL",
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
                "is_approved": user.is_approved
            }
        }

    # LOGIN SUCCESS

    return {
        "success": True,
        "status_code": 200,
        "message": "Login successful.",
        "session_created": True,
        "data": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_approved": user.is_approved
        }
    }