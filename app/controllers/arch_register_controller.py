import os
import uuid
import shutil

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.arch_register_model import ArchRegister

ALLOWED_ROLES = [
    "admin",
    "architect",
    "sales_person"
]

# Where profile images are saved on disk
PROFILE_IMAGE_DIR = "static/profile_images"
os.makedirs(PROFILE_IMAGE_DIR, exist_ok=True)


# ── REGISTER USER ────────────────────────────────────────────

def create_arch_register_user(payload, db: Session):

    existing_user = (
        db.query(ArchRegister)
        .filter(ArchRegister.email == payload.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if payload.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    is_approved = payload.role != "architect"

    user = ArchRegister(
        role=payload.role,
        is_approved=is_approved,
        full_name=payload.full_name,
        firm_name=payload.firm_name,
        mobile_number=payload.mobile_number,
        email=payload.email,
        date_of_birth=payload.date_of_birth,
        profession=payload.profession,
        marital_status=payload.marital_status,
        anniversary_date=payload.anniversary_date,
        account_holder_name=payload.account_holder_name,
        bank_name=payload.bank_name,
        account_number=payload.account_number,
        ifsc_code=payload.ifsc_code,
        upi_id=payload.upi_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

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


# ── GET ALL USERS ────────────────────────────────────────────

def get_arch_register_users(db: Session):

    users = db.query(ArchRegister).all()

    return {
        "success": True,
        "count": len(users),
        "data": users
    }


# ── APPROVE ARCHITECT ────────────────────────────────────────

def approve_architect_user(user_id: int, db: Session):

    user = (
        db.query(ArchRegister)
        .filter(ArchRegister.id == user_id)
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


# ── LOGIN USER ───────────────────────────────────────────────

def login_user(email: str, db: Session):

    user = (
        db.query(ArchRegister)
        .filter(ArchRegister.email == email)
        .first()
    )

    if not user:
        return {
            "success": False,
            "status_code": 404,
            "message": "Account not found.",
            "error": "USER_NOT_FOUND",
            "data": None
        }

    if user.role == "architect" and not user.is_approved:
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


# ── UPDATE USER (PATCH) ──────────────────────────────────────

CATEGORY_FIELDS = {
    "personal": [
        "full_name",
        "mobile_number",
        "email",
        "date_of_birth",
        "marital_status",
    ],
    "professional": [
        "profession",
        "firm_name",
    ],
    "bank": [
        "bank_name",
        "account_holder_name",
        "account_number",
        "ifsc_code",
        "upi_id",
    ],
}


def _build_response_data(user: ArchRegister) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_approved": user.is_approved,
        "mobile_number": user.mobile_number,
        "date_of_birth": str(user.date_of_birth) if user.date_of_birth else None,
        "marital_status": user.marital_status,
        "profession": user.profession,
        "firm_name": user.firm_name,
        "bank_name": user.bank_name,
        "account_holder_name": user.account_holder_name,
        "account_number": user.account_number,
        "ifsc_code": user.ifsc_code,
        "upi_id": user.upi_id,
        "profile_image": user.profile_image,
    }


def update_arch_user(
    user_id: int,
    category: str,
    payload,
    db: Session
):

    if category not in CATEGORY_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Allowed: {list(CATEGORY_FIELDS.keys())}"
        )

    user = (
        db.query(ArchRegister)
        .filter(ArchRegister.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    allowed = CATEGORY_FIELDS[category]
    incoming = payload.model_dump(exclude_unset=True)
    updated_fields = []

    for field, value in incoming.items():
        if field in allowed:
            setattr(user, field, value)
            updated_fields.append(field)

    if not updated_fields:
        raise HTTPException(
            status_code=400,
            detail="No valid fields provided for this category"
        )

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": f"{category.capitalize()} details updated successfully",
        "updated_fields": updated_fields,
        "data": _build_response_data(user)
    }


# ── UPLOAD PROFILE IMAGE ─────────────────────────────────────

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_SIZE_MB = 5


def upload_profile_image(user_id: int, file: UploadFile, db: Session):

    user = (
        db.query(ArchRegister)
        .filter(ArchRegister.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: JPEG, PNG, WEBP"
        )

    # Delete old image from disk if it exists
    if user.profile_image:
        old_path = user.profile_image.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    # Save new image with a unique filename
    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(PROFILE_IMAGE_DIR, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Check file size after saving
    size_mb = os.path.getsize(save_path) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        os.remove(save_path)
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_IMAGE_SIZE_MB} MB."
        )

    # Store relative URL path in DB
    image_url = f"/static/profile_images/{filename}"
    user.profile_image = image_url
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Profile image uploaded successfully",
        "data": {
            "id": user.id,
            "profile_image": user.profile_image
        }
    }
