from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

ARCH_SECRET_KEY = "CHANGE_THIS_SECRET_KEY"
ARCH_ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def arch_hash_password(password: str):
    return pwd_context.hash(password)


def arch_verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def arch_create_access_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire})

    return jwt.encode(payload, ARCH_SECRET_KEY, algorithm=ARCH_ALGORITHM)