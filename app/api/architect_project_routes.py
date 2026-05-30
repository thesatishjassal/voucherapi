from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import (
    get_db_connection
)

from app.schema.architect_project_schema import (
    CreateProjectSchema,
    UpdateProjectSchema
)

from app.controllers.architect_project_controller import (
    create_project,
    get_my_projects,
    get_project_by_id,
    update_project,
    delete_project
)

router = APIRouter(
    prefix="/api/projects",
    tags=["Architect Projects"]
)


# CREATE PROJECT

@router.post("/{architect_id}")
def add_project(
    architect_id: int,
    payload: CreateProjectSchema,
    db: Session = Depends(
        get_db_connection
    )
):

    return create_project(
        architect_id,
        payload,
        db
    )


# GET ALL MY PROJECTS

@router.get("/{architect_id}")
def my_projects(
    architect_id: int,
    db: Session = Depends(
        get_db_connection
    )
):

    return get_my_projects(
        architect_id,
        db
    )


# GET SINGLE PROJECT

@router.get(
    "/{architect_id}/{project_id}"
)
def get_project(
    architect_id: int,
    project_id: int,
    db: Session = Depends(
        get_db_connection
    )
):

    return get_project_by_id(
        project_id,
        architect_id,
        db
    )


# UPDATE PROJECT

@router.put(
    "/{architect_id}/{project_id}"
)
def edit_project(
    architect_id: int,
    project_id: int,
    payload: UpdateProjectSchema,
    db: Session = Depends(
        get_db_connection
    )
):

    return update_project(
        project_id,
        architect_id,
        payload,
        db
    )


# DELETE PROJECT

@router.delete(
    "/{architect_id}/{project_id}"
)
def remove_project(
    architect_id: int,
    project_id: int,
    db: Session = Depends(
        get_db_connection
    )
):

    return delete_project(
        project_id,
        architect_id,
        db
    )