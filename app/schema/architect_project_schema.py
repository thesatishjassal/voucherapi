from pydantic import BaseModel
from typing import Optional
from datetime import date


class CreateProjectSchema(BaseModel):
    title: str
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "In Progress"
    image_url: Optional[str] = None

    # New Fields
    client: Optional[str] = None
    budget: Optional[float] = None
    date: Optional[date] = None


class UpdateProjectSchema(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None

    # New Fields
    client: Optional[str] = None
    budget: Optional[float] = None
    date: Optional[date] = None


class ProjectResponseSchema(BaseModel):
    id: int
    architect_id: int
    title: str
    location: Optional[str]
    description: Optional[str]
    status: Optional[str]
    image_url: Optional[str]

    # New Fields
    client: Optional[str]
    budget: Optional[float]
    date: Optional[date]

    class Config:
        orm_mode = True