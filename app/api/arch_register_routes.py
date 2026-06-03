from fastapi import (
    APIRouter,
    Depends,
    Body,
    Path,
    Query
)

from sqlalchemy.orm import Session

from database import get_db_connection

from app.schema.arch_register_schema import (
    ArchRegisterSchema,
    UpdatePersonalSchema,
    UpdateProfessionalSchema,
    UpdateBankSchema,
)

from app.controllers.arch_register_controller import (
    create_arch_register_user,
    get_arch_register_users,
    approve_architect_user,
    login_user,
    update_arch_user,
)

router = APIRouter(
    prefix="/api/arch-register",
    tags=["Arch Register"]
)

# SCHEMA MAP — routes to the correct Pydantic schema per category
CATEGORY_SCHEMA = {
    "personal":     UpdatePersonalSchema,
    "professional": UpdateProfessionalSchema,
    "bank":         UpdateBankSchema,
}


# ── REGISTER USER ────────────────────────────────────────────

@router.post("/")
def register_user(
    payload: ArchRegisterSchema,
    db: Session = Depends(get_db_connection)
):
    return create_arch_register_user(payload, db)


# ── GET ALL USERS ────────────────────────────────────────────

@router.get("/")
def get_users(
    db: Session = Depends(get_db_connection)
):
    return get_arch_register_users(db)


# ── APPROVE ARCHITECT ────────────────────────────────────────

@router.put("/approve/{user_id}")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db_connection)
):
    return approve_architect_user(user_id, db)


# ── LOGIN USER ───────────────────────────────────────────────

@router.post("/login")
def login(
    email: str = Body(...),
    db: Session = Depends(get_db_connection)
):
    return login_user(email, db)


# ── UPDATE USER (PATCH) ──────────────────────────────────────

@router.patch("/{user_id}/update")
def update_user(
    user_id: int = Path(...),
    category: str = Query(
        ...,
        description="personal | professional | bank"
    ),
    body: dict = Body(...),
    db: Session = Depends(get_db_connection)
):
    SchemaClass = CATEGORY_SCHEMA.get(category)

    if not SchemaClass:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Invalid category. Allowed: personal, professional, bank"
        )

    payload = SchemaClass(**body)

    return update_arch_user(user_id, category, payload, db)