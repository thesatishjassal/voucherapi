from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection

from app.controllers.salesperson_controller import SalesPersonController

from app.schema.salesperson import (
    SalesPersonCreate,
    SalesPersonUpdate,
    SalesPersonSendOtp,
    SalesPersonVerifyOtp,
)

router = APIRouter(
    prefix="/salespersons",
    tags=["Salespersons"]
)


# --------------------------------------------------------
# Create
# --------------------------------------------------------

@router.post("/")
def create_salesperson(
    payload: SalesPersonCreate,
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.create(db, payload)


# --------------------------------------------------------
# Send OTP
# --------------------------------------------------------

@router.post("/send-otp")
def send_otp(
    payload: SalesPersonSendOtp,
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.send_otp(
        db,
        payload
    )


# --------------------------------------------------------
# Verify OTP
# --------------------------------------------------------

@router.post("/verify-otp")
def verify_otp(
    payload: SalesPersonVerifyOtp,
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.verify_otp(
        db,
        payload
    )


# --------------------------------------------------------
# Get All
# --------------------------------------------------------

@router.get("/")
def get_all_salespersons(
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.get_all(db)


# --------------------------------------------------------
# Get By ID
# --------------------------------------------------------

@router.get("/{salesperson_id}")
def get_salesperson(
    salesperson_id: int,
    db: Session = Depends(get_db_connection)
):

    salesperson = SalesPersonController.get_by_id(
        db,
        salesperson_id
    )

    if not salesperson:
        raise HTTPException(
            status_code=404,
            detail="Salesperson not found"
        )

    return salesperson


# --------------------------------------------------------
# Update
# --------------------------------------------------------

@router.put("/{salesperson_id}")
def update_salesperson(
    salesperson_id: int,
    payload: SalesPersonUpdate,
    db: Session = Depends(get_db_connection)
):

    salesperson = SalesPersonController.update(
        db,
        salesperson_id,
        payload
    )

    if not salesperson:
        raise HTTPException(
            status_code=404,
            detail="Salesperson not found"
        )

    return salesperson


# --------------------------------------------------------
# Delete
# --------------------------------------------------------

@router.delete("/{salesperson_id}")
def delete_salesperson(
    salesperson_id: int,
    db: Session = Depends(get_db_connection)
):

    deleted = SalesPersonController.delete(
        db,
        salesperson_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Salesperson not found"
        )

    return {
        "success": True,
        "message": "Salesperson deleted successfully."
    }