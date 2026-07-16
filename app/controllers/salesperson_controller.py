import random
from datetime import datetime, timedelta

from fastapi import HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm import Session

from app.models.salesperson import SalesPerson
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "panviklighting@gmail.com"
SMTP_PASS = "dshwxchuudwjvixs"
# Replace this with your actual email sender
def send_otp_email(email: str, name: str, otp: str):

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Panvik Partner Login OTP</title>
</head>

<body style="margin:0;padding:0;background:#F4F6F9;font-family:Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
<tr>
<td align="center">

<table width="560" cellpadding="0" cellspacing="0"
style="background:#ffffff;border-radius:16px;overflow:hidden;">

<tr>
<td style="background:#111827;padding:30px;">

<h2 style="margin:0;color:#ffffff;">
Panvik Partner Portal
</h2>

<p style="margin-top:8px;color:#D1D5DB;">
Secure Login Verification
</p>

</td>
</tr>

<tr>
<td style="padding:35px;">

<p style="font-size:16px;color:#111827;">
Hi <strong>{name}</strong>,
</p>

<p style="color:#4B5563;line-height:1.7;">
Use the following One-Time Password (OTP) to securely sign in to your Panvik Partner account.
</p>

<div style="
margin:35px 0;
text-align:center;
">

<div style="
display:inline-block;
padding:18px 36px;
background:#F3F4F6;
border:2px dashed #D1D5DB;
border-radius:12px;
font-size:34px;
font-weight:700;
letter-spacing:10px;
color:#111827;
">
{otp}
</div>

</div>

<p style="color:#EF4444;font-weight:600;">
This OTP is valid for 10 minutes.
</p>

<p style="color:#6B7280;">
Never share this OTP with anyone.
Panvik will never ask for your OTP over phone or email.
</p>

<hr style="border:none;border-top:1px solid #E5E7EB;margin:35px 0;">

<p style="font-size:12px;color:#9CA3AF;">
If you didn't request this login, you can safely ignore this email.
</p>

<p style="font-size:12px;color:#9CA3AF;">
© {datetime.now().year} Panvik Lighting
</p>

</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""

    text_body = f"""
Panvik Partner Portal

Hello {name},

Your Login OTP is:

{otp}

This OTP is valid for 10 minutes.

If you didn't request this login, ignore this email.

Panvik Lighting
"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Panvik Login OTP"
    message["From"] = f"Panvik Lighting <{SMTP_USER}>"
    message["To"] = email

    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(
            SMTP_USER,
            email,
            message.as_string()
        )


class SalesPersonController:

    @staticmethod
    def create(db: Session, payload):
        try:
            salesperson = SalesPerson(**payload.dict())

            db.add(salesperson)
            db.commit()
            db.refresh(salesperson)

            return salesperson

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail={
                    "email": "This email is already registered."
                }
            )

    # --------------------------------------------------------
    # Send OTP
    # --------------------------------------------------------

    @staticmethod
    def send_otp(db: Session, payload):

        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.email == payload.email)
            .first()
        )

        if not salesperson:
            return {
                "success": False,
                "error": "USER_NOT_FOUND",
                "message": "No account found with this email."
            }

        otp = "".join(
            random.choices(
                "0123456789",
                k=OTP_LENGTH
            )
        )

        salesperson.otp = otp
        salesperson.otp_expires_at = (
            datetime.utcnow() +
            timedelta(minutes=OTP_VALID_MINUTES)
        )

        db.commit()

        send_otp_email(
            salesperson.email,
            otp
        )

        return {
            "success": True,
            "message": "OTP sent successfully."
        }

    # --------------------------------------------------------
    # Verify OTP
    # --------------------------------------------------------

    @staticmethod
    def verify_otp(db: Session, payload):

        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.email == payload.email)
            .first()
        )

        if not salesperson:
            return {
                "success": False,
                "error": "USER_NOT_FOUND",
                "message": "No account found with this email."
            }

        if not salesperson.otp:
            return {
                "success": False,
                "error": "OTP_NOT_REQUESTED",
                "message": "Please request an OTP first."
            }

        if salesperson.otp_expires_at < datetime.utcnow():
            return {
                "success": False,
                "error": "OTP_EXPIRED",
                "message": "OTP has expired."
            }

        if salesperson.otp != payload.otp:
            return {
                "success": False,
                "error": "INVALID_OTP",
                "message": "Invalid OTP."
            }

        salesperson.otp = None
        salesperson.otp_expires_at = None

        db.commit()

        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "id": salesperson.id,
                "name": salesperson.name,
                "email": salesperson.email,
                "phone": salesperson.phone,
                "architecture_name": salesperson.architecture_name,
                "company_name": salesperson.company_name,
            }
        }

    # --------------------------------------------------------
    # Get All
    # --------------------------------------------------------

    @staticmethod
    def get_all(db: Session):
        return db.query(SalesPerson).all()

    # --------------------------------------------------------
    # Get By ID
    # --------------------------------------------------------

    @staticmethod
    def get_by_id(db: Session, salesperson_id: int):

        return (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    @staticmethod
    def update(db: Session, salesperson_id: int, payload):

        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return None

        update_data = payload.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(salesperson, key, value)

        db.commit()
        db.refresh(salesperson)

        return salesperson

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    @staticmethod
    def delete(db: Session, salesperson_id: int):

        salesperson = (
            db.query(SalesPerson)
            .filter(SalesPerson.id == salesperson_id)
            .first()
        )

        if not salesperson:
            return False

        db.delete(salesperson)
        db.commit()

        return True