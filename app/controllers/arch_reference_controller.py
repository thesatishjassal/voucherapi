from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.arch_register_model import ArchRegister
from app.models.arch_register_model  import ArchReference


# ── HELPERS ──────────────────────────────────────────────────

def _get_user_or_404(user_id: int, db: Session) -> ArchRegister:
    user = db.query(ArchRegister).filter(ArchRegister.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _build_reference_data(ref: ArchReference) -> dict:
    return {
        "id": ref.id,
        "sales_person_id": ref.sales_person_id,
        "architect_id": ref.architect_id,
        "notes": ref.notes,
        "added_at": str(ref.added_at),
        "architect": {
            "id": ref.architect.id,
            "full_name": ref.architect.full_name,
            "email": ref.architect.email,
            "mobile_number": ref.architect.mobile_number,
            "firm_name": ref.architect.firm_name,
            "profession": ref.architect.profession,
            "profile_image": ref.architect.profile_image,
        } if ref.architect else None,
        "sales_person": {
            "id": ref.sales_person.id,
            "full_name": ref.sales_person.full_name,
            "email": ref.sales_person.email,
            "mobile_number": ref.sales_person.mobile_number,
        } if ref.sales_person else None,
    }


# ── ADD REFERENCE ────────────────────────────────────────────

def add_arch_reference(sales_person_id: int, payload, db: Session):
    """
    A salesperson (sales_person_id) adds an architect (payload.architect_id)
    to their reference list.
    """

    # 1. Validate salesperson exists and has the right role
    sales_person = _get_user_or_404(sales_person_id, db)
    if sales_person.role != "sales_person":
        raise HTTPException(
            status_code=403,
            detail="Only sales persons can add architect references"
        )

    # 2. Validate the architect exists and is actually an architect
    architect = _get_user_or_404(payload.architect_id, db)
    if architect.role != "architect":
        raise HTTPException(
            status_code=400,
            detail="The referenced user is not an architect"
        )

    # 3. Prevent duplicate references
    existing = (
        db.query(ArchReference)
        .filter(
            ArchReference.sales_person_id == sales_person_id,
            ArchReference.architect_id == payload.architect_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already added this architect to your references"
        )

    # 4. Create the reference
    reference = ArchReference(
        sales_person_id=sales_person_id,
        architect_id=payload.architect_id,
        notes=payload.notes,
    )

    db.add(reference)
    db.commit()
    db.refresh(reference)

    return {
        "success": True,
        "message": "Architect reference added successfully",
        "data": _build_reference_data(reference)
    }


# ── GET ALL REFERENCES FOR A SALESPERSON ─────────────────────

def get_references_by_sales_person(sales_person_id: int, db: Session):
    """Return all architects a salesperson has referenced."""

    sales_person = _get_user_or_404(sales_person_id, db)
    if sales_person.role != "sales_person":
        raise HTTPException(
            status_code=403,
            detail="Only sales persons have reference lists"
        )

    references = (
        db.query(ArchReference)
        .filter(ArchReference.sales_person_id == sales_person_id)
        .all()
    )

    return {
        "success": True,
        "sales_person_id": sales_person_id,
        "count": len(references),
        "data": [_build_reference_data(r) for r in references]
    }


# ── GET ALL SALESPERSONS WHO REFERENCED AN ARCHITECT ─────────

def get_sales_persons_for_architect(architect_id: int, db: Session):
    """Return all salespersons who have added this architect as a reference."""

    architect = _get_user_or_404(architect_id, db)
    if architect.role != "architect":
        raise HTTPException(
            status_code=400,
            detail="The given user is not an architect"
        )

    references = (
        db.query(ArchReference)
        .filter(ArchReference.architect_id == architect_id)
        .all()
    )

    return {
        "success": True,
        "architect_id": architect_id,
        "count": len(references),
        "data": [_build_reference_data(r) for r in references]
    }


# ── UPDATE REFERENCE NOTES ────────────────────────────────────

def update_arch_reference(sales_person_id: int, reference_id: int, payload, db: Session):

    reference = (
        db.query(ArchReference)
        .filter(
            ArchReference.id == reference_id,
            ArchReference.sales_person_id == sales_person_id,
        )
        .first()
    )

    if not reference:
        raise HTTPException(
            status_code=404,
            detail="Reference not found or does not belong to this sales person"
        )

    if payload.notes is not None:
        reference.notes = payload.notes

    db.commit()
    db.refresh(reference)

    return {
        "success": True,
        "message": "Reference updated successfully",
        "data": _build_reference_data(reference)
    }


# ── DELETE REFERENCE ──────────────────────────────────────────

def delete_arch_reference(sales_person_id: int, reference_id: int, db: Session):

    reference = (
        db.query(ArchReference)
        .filter(
            ArchReference.id == reference_id,
            ArchReference.sales_person_id == sales_person_id,
        )
        .first()
    )

    if not reference:
        raise HTTPException(
            status_code=404,
            detail="Reference not found or does not belong to this sales person"
        )

    db.delete(reference)
    db.commit()

    return {
        "success": True,
        "message": "Reference removed successfully"
    }
