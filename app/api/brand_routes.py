from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db_connection
from app.schema.brand_qr import BrandCreate

from app.controllers.brand_controller import (
    create_brand_controller,
    get_all_brands_controller,
    get_brand_by_name_controller,
    update_brand_controller,
    delete_brand_controller
)

router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)


# CREATE
@router.post("/")
def create_brand(
    data: BrandCreate,
    db: Session = Depends(get_db_connection)
):
    return create_brand_controller(data, db)


# GET ALL
@router.get("/")
def get_all_brands(
    db: Session = Depends(get_db_connection)
):
    return get_all_brands_controller(db)


# GET BY BRAND NAME
@router.get("/{brand_name}")
def get_brand_by_name(
    brand_name: str,
    db: Session = Depends(get_db_connection)
):
    return get_brand_by_name_controller(
        brand_name,
        db
    )


# UPDATE
@router.put("/{id}")
def update_brand(
    id: int,
    data: BrandCreate,
    db: Session = Depends(get_db_connection)
):
    return update_brand_controller(
        id,
        data,
        db
    )


# DELETE
@router.delete("/{id}")
def delete_brand(
    id: int,
    db: Session = Depends(get_db_connection)
):
    return delete_brand_controller(id, db)