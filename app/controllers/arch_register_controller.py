import os
import uuid
import shutil

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.arch_register_model import ArchRegister
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

ALLOWED_ROLES = [
    "admin",
    "architect",
    "sales_person"
]

ADMIN_EMAIL = "tusharguglani19@gmail.com"
ADMIN_APPROVAL_LINK = "https://partners.panvik.com/admin"

# ── Put your SMTP credentials in env vars ──
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tusharguglani19@gmail.com"   # replace or load from os.environ
SMTP_PASS = "hzsigcffytfmgylg"
   
# Where profile images are saved on disk
PROFILE_IMAGE_DIR = "static/profile_images"
os.makedirs(PROFILE_IMAGE_DIR, exist_ok=True)


# ── REGISTER USER ────────────────────────────────────────────

def send_admin_approval_email(user_full_name: str, user_email: str, user_mobile: str, firm_name: str):
    """Send a beautifully formatted approval-request email to the admin."""

    registered_at = datetime.now().strftime("%d %b %Y, %I:%M %p")

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>New Architect Registration</title>
</head>
<body style="margin:0;padding:0;background:#F4F6F9;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4F6F9;padding:40px 16px;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="560" cellpadding="0" cellspacing="0" border="0"
               style="background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);max-width:560px;width:100%;">

          <!-- Header band -->
          <tr>
            <td style="background:#111827;padding:32px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <p style="margin:0;font-size:12px;font-weight:700;letter-spacing:0.12em;color:#9CA3AF;text-transform:uppercase;">Panvik Lighting</p>
                    <h1 style="margin:8px 0 0;font-size:22px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">
                      New Architect Registered
                    </h1>
                  </td>
                  <td align="right" valign="middle">
                    <div style="width:48px;height:48px;background:#1F2937;border-radius:12px;text-align:center;line-height:48px;font-size:24px;">
                      🏛️
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Alert pill -->
          <tr>
            <td style="padding:24px 36px 0;">
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:99px;padding:6px 16px;">
                    <span style="font-size:12.5px;font-weight:700;color:#92400E;">⏳ &nbsp;Awaiting Your Approval</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body text -->
          <tr>
            <td style="padding:20px 36px 0;">
              <p style="margin:0;font-size:15px;color:#374151;line-height:1.65;">
                A new architect has registered on the Panvik Partner Portal and is waiting for your approval before they can access the platform.
              </p>
            </td>
          </tr>

          <!-- Details card -->
          <tr>
            <td style="padding:24px 36px 0;">
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#F9FAFB;border-radius:14px;border:1px solid #F3F4F6;overflow:hidden;">

                <!-- Section label -->
                <tr>
                  <td colspan="2" style="padding:14px 20px 10px;">
                    <p style="margin:0;font-size:11px;font-weight:700;letter-spacing:0.08em;color:#9CA3AF;text-transform:uppercase;">
                      Architect Details
                    </p>
                  </td>
                </tr>

                <!-- Row: Name -->
                <tr style="border-top:1px solid #F3F4F6;">
                  <td style="padding:12px 20px;width:38%;vertical-align:top;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;font-weight:600;">Full Name</p>
                  </td>
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:14px;color:#111827;font-weight:700;">{user_full_name}</p>
                  </td>
                </tr>

                <!-- Row: Email -->
                <tr style="border-top:1px solid #F3F4F6;">
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;font-weight:600;">Email</p>
                  </td>
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:14px;color:#111827;">{user_email}</p>
                  </td>
                </tr>

                <!-- Row: Mobile -->
                <tr style="border-top:1px solid #F3F4F6;">
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;font-weight:600;">Mobile</p>
                  </td>
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:14px;color:#111827;">{user_mobile or "—"}</p>
                  </td>
                </tr>

                <!-- Row: Firm -->
                <tr style="border-top:1px solid #F3F4F6;">
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;font-weight:600;">Firm</p>
                  </td>
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:14px;color:#111827;">{firm_name or "Independent"}</p>
                  </td>
                </tr>

                <!-- Row: Registered at -->
                <tr style="border-top:1px solid #F3F4F6;">
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;font-weight:600;">Registered</p>
                  </td>
                  <td style="padding:12px 20px;vertical-align:top;">
                    <p style="margin:0;font-size:14px;color:#111827;">{registered_at}</p>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- CTA Button -->
          <tr>
            <td style="padding:28px 36px 8px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <a href="{ADMIN_APPROVAL_LINK}"
                       style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;
                              font-size:15px;font-weight:700;letter-spacing:-0.2px;
                              padding:15px 40px;border-radius:12px;
                              border:none;cursor:pointer;">
                      Review &amp; Approve →
                    </a>
                  </td>
                </tr>
                <tr>
                  <td align="center" style="padding-top:12px;">
                    <p style="margin:0;font-size:12px;color:#9CA3AF;">
                      Or copy this link:
                      <a href="{ADMIN_APPROVAL_LINK}"
                         style="color:#6366F1;text-decoration:none;font-weight:600;">
                        {ADMIN_APPROVAL_LINK}
                      </a>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:24px 36px 0;">
              <div style="height:1px;background:#F3F4F6;"></div>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:20px 36px 32px;">
              <p style="margin:0;font-size:12px;color:#9CA3AF;line-height:1.6;">
                This email was sent automatically when a new architect registered on the Panvik Partner Portal.
                You are receiving this because you are the account administrator.
              </p>
              <p style="margin:10px 0 0;font-size:12px;color:#D1D5DB;">
                © {datetime.now().year} Panvik Lighting &nbsp;·&nbsp; Partner Portal
              </p>
            </td>
          </tr>

        </table>
        <!-- /Card -->

      </td>
    </tr>
  </table>

</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🏛️ New Architect Registration — {user_full_name} needs approval"
    msg["From"] = f"Panvik Portal <{SMTP_USER}>"
    msg["To"] = ADMIN_EMAIL

    # Plain-text fallback
    text_body = f"""New Architect Registration — Action Required

Name:       {user_full_name}
Email:      {user_email}
Mobile:     {user_mobile or "—"}
Firm:       {firm_name or "Independent"}
Registered: {registered_at}

Click here to approve: {ADMIN_APPROVAL_LINK}

This email was sent automatically by the Panvik Partner Portal.
"""

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, ADMIN_EMAIL, msg.as_string())


# ─────────────────────────────────────────────────────────────
# Registration handler
# ─────────────────────────────────────────────────────────────

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

    # ── Send admin notification for architects ──
    if user.role == "architect":
        try:
            send_admin_approval_email(
                user_full_name=user.full_name,
                user_email=user.email,
                user_mobile=user.mobile_number,
                firm_name=user.firm_name,
            )
        except Exception as e:
            # Don't fail registration if email fails — just log it
            print(f"[WARN] Admin email failed: {e}")

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
