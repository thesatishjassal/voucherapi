from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.arch_register_model import (
    ArchRegister
)

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

    user = ArchRegister(

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

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }

def get_arch_register_users(
    db: Session
):

    users = db.query(ArchRegister).all()

    return users