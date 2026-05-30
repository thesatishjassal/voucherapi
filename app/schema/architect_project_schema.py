from pydantic import BaseModel
from typing import Optional


class CreateProjectSchema(BaseModel):

    title: str

    location: Optional[str] = None

    description: Optional[str] = None

    status: Optional[str] = "In Progress"

    image_url: Optional[str] = None


class UpdateProjectSchema(BaseModel):

    title: str

    location: Optional[str] = None

    description: Optional[str] = None

    status: Optional[str] = None

    image_url: Optional[str] = None


class ProjectResponseSchema(BaseModel):

    id: int

    architect_id: int

    title: str

    location: Optional[str]

    description: Optional[str]

    status: Optional[str]

    image_url: Optional[str]

    class Config:
        orm_mode = True