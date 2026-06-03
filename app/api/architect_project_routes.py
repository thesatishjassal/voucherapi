from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid
from datetime import date

from database import get_db_connection
from app.controllers.architect_project_controller import (
    create_project, get_my_projects, get_project_by_id,
    update_project, delete_project
)

router = APIRouter(prefix="/api/projects", tags=["Architect Projects"])

UPLOAD_DIR = Path("uploads/projects")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_image(image: UploadFile) -> str:
    if not image:
        return None
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, detail="Only image files are allowed")

    file_ext = image.filename.split(".")[-1].lower()
    unique_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / unique_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f"uploads/projects/{unique_name}"


# ===================== CREATE =====================
@router.post("/{architect_id}")
async def add_project(
    architect_id: int,
    title: str = Form(...),
    location: str = Form(None),
    description: str = Form(None),
    status: str = Form("In Progress"),
    client: str = Form(None),
    budget: float = Form(None),
    date: date = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db_connection)
):
    image_url = save_uploaded_image(image)

    payload = type('obj', (object,), {
        'title': title,
        'location': location,
        'description': description,
        'status': status,
        'image_url': image_url,
        'client': client,
        'budget': budget,
        'date': date
    })()

    return create_project(architect_id, payload, db)


# ===================== UPDATE =====================
@router.put("/{architect_id}/{project_id}")
async def edit_project(
    architect_id: int,
    project_id: int,
    title: str = Form(None),
    location: str = Form(None),
    description: str = Form(None),
    status: str = Form(None),
    client: str = Form(None),
    budget: float = Form(None),
    date: date = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db_connection)
):
    image_url = save_uploaded_image(image)

    payload = type('obj', (object,), {
        'title': title,
        'location': location,
        'description': description,
        'status': status,
        'image_url': image_url,
        'client': client,
        'budget': budget,
        'date': date
    })()

    return update_project(project_id, architect_id, payload, db)


# GET & DELETE remain same
@router.get("/{architect_id}")
def my_projects(architect_id: int, db: Session = Depends(get_db_connection)):
    return get_my_projects(architect_id, db)


@router.get("/{architect_id}/{project_id}")
def get_project(architect_id: int, project_id: int, db: Session = Depends(get_db_connection)):
    return get_project_by_id(project_id, architect_id, db)
 

@router.delete("/{architect_id}/{project_id}")
def remove_project(architect_id: int, project_id: int, db: Session = Depends(get_db_connection)):
    return delete_project(project_id, architect_id, db)