from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db_connection
from app.controllers.salesperson_controller import SalesPersonController
from app.schema.salesperson import (
    SalesPersonCreate,
    SalesPersonUpdate
)

router = APIRouter(
    prefix="/salespersons",
    tags=["Salespersons"]
)


@router.post("/")
def create_salesperson(
    payload: SalesPersonCreate,
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.create(db, payload)


@router.get("/")
def get_all_salespersons(
    db: Session = Depends(get_db_connection)
):
    return SalesPersonController.get_all(db)


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
        "message": "Salesperson deleted successfully"
    }