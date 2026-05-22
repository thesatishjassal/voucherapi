from sqlalchemy.orm import Session
from app.models.arch_user import ArchUser
from app.utils.arch_security import (
    arch_verify_password,
    arch_create_access_token
)


def arch_authenticate_user(db: Session, email: str, password: str):
    user = db.query(ArchUser).filter(ArchUser.email == email).first()

    if not user:
        return None

    if not arch_verify_password(password, user.password):
        return None

    return user


def arch_login_user(db: Session, email: str, password: str):
    user = arch_authenticate_user(db, email, password)

    if not user:
        return None

    token = arch_create_access_token(
        {"user_id": user.id, "email": user.email}
    )

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
        },
    }