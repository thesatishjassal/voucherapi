from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db_connection
from app.schema.arch_reference_schema import AddArchReferenceSchema, UpdateArchReferenceSchema
from app.controllers.arch_reference_controller import (
    add_arch_reference,
    get_references_by_sales_person,
    get_sales_persons_for_architect,
    update_arch_reference,
    delete_arch_reference,
)

router = APIRouter(prefix="/references", tags=["Arch References"])


# POST /references/sales/{sales_person_id}
# Salesperson adds an architect to their reference list
@router.post("/sales/{sales_person_id}")
def add_reference(
    sales_person_id: int,
    payload: AddArchReferenceSchema,
    db: Session = Depends(get_db)
):
    return add_arch_reference(sales_person_id, payload, db)


# GET /references/sales/{sales_person_id}
# Get all architects referenced by a salesperson
@router.get("/sales/{sales_person_id}")
def get_my_references(
    sales_person_id: int,
    db: Session = Depends(get_db)
):
    return get_references_by_sales_person(sales_person_id, db)


# GET /references/architect/{architect_id}
# Get all salespersons who have referenced this architect
@router.get("/architect/{architect_id}")
def get_architect_references(
    architect_id: int,
    db: Session = Depends(get_db)
):
    return get_sales_persons_for_architect(architect_id, db)


# PATCH /references/sales/{sales_person_id}/{reference_id}
# Update notes on a reference
@router.patch("/sales/{sales_person_id}/{reference_id}")
def update_reference(
    sales_person_id: int,
    reference_id: int,
    payload: UpdateArchReferenceSchema,
    db: Session = Depends(get_db)
):
    return update_arch_reference(sales_person_id, reference_id, payload, db)


# DELETE /references/sales/{sales_person_id}/{reference_id}
# Remove a reference
@router.delete("/sales/{sales_person_id}/{reference_id}")
def delete_reference(
    sales_person_id: int,
    reference_id: int,
    db: Session = Depends(get_db)
):
    return delete_arch_reference(sales_person_id, reference_id, db)
