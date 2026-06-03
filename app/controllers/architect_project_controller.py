from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.architect_project_model import ArchitectProject


# CREATE PROJECT
def create_project(architect_id: int, payload, db: Session):
    project = ArchitectProject(
        architect_id=architect_id,
        title=payload.title,
        location=payload.location,
        description=payload.description,
        status=payload.status,
        image_url=payload.image_url,
        client=payload.client,
        budget=payload.budget,
        date=payload.date,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "success": True,
        "message": "Project created successfully",
        "data": project
    }


# GET MY PROJECTS
def get_my_projects(architect_id: int, db: Session):
    projects = (
        db.query(ArchitectProject)
        .filter(ArchitectProject.architect_id == architect_id)
        .all()
    )
    return {
        "success": True,
        "count": len(projects),
        "data": projects
    }


# GET SINGLE PROJECT
def get_project_by_id(project_id: int, architect_id: int, db: Session):
    project = (
        db.query(ArchitectProject)
        .filter(
            ArchitectProject.id == project_id,
            ArchitectProject.architect_id == architect_id
        )
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"success": True, "data": project}


# UPDATE PROJECT
def update_project(project_id: int, architect_id: int, payload, db: Session):
    project = db.query(ArchitectProject).filter(
        ArchitectProject.id == project_id,
        ArchitectProject.architect_id == architect_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if payload.title is not None:
        project.title = payload.title
    if payload.location is not None:
        project.location = payload.location
    if payload.description is not None:
        project.description = payload.description
    if payload.status is not None:
        project.status = payload.status
    if payload.image_url is not None:
        project.image_url = payload.image_url
    if payload.client is not None:
        project.client = payload.client
    if payload.budget is not None:
        project.budget = payload.budget
    if payload.date is not None:
        project.date = payload.date

    db.commit()
    db.refresh(project)

    return {
        "success": True,
        "message": "Project updated successfully",
        "data": project
    }


# DELETE PROJECT (unchanged)
def delete_project(project_id: int, architect_id: int, db: Session):
    project = db.query(ArchitectProject).filter(
        ArchitectProject.id == project_id,
        ArchitectProject.architect_id == architect_id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"success": True, "message": "Project deleted successfully"}