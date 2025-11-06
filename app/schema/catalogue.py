from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CatalogueBase(BaseModel):
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    google_drive_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CatalogueCreate(CatalogueBase):
    created_by: str  # Required for creation

class CatalogueUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    google_drive_url: Optional[str] = None
    created_by: Optional[str] = None  # Optional for updates (e.g., if reassigning)

class CatalogueResponse(CatalogueBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CatalogueDeleteResponse(BaseModel):
    message: str
    id: int

    model_config = ConfigDict(from_attributes=True)