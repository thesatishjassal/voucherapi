import random
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -------------------------
# GENERATE OTP
# -------------------------
def generate_otp():
    return str(
        random.randint(100000, 999999)
    )

# -------------------------
# HASH OTP
# -------------------------
def hash_otp(otp: str):
    return pwd_context.hash(otp)

# -------------------------
# VERIFY OTP
# -------------------------
def verify_otp(
    plain_otp: str,
    hashed_otp: str
):
    return pwd_context.verify(
        plain_otp,
        hashed_otp
    )