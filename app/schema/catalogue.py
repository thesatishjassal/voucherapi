from pydantic import BaseModel, ConfigDict  # Add ConfigDict for v2 best practices
from datetime import datetime
from typing import Optional

class CatalogueBase(BaseModel):
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)  # Global config for base (propagates)

class CatalogueCreate(CatalogueBase):   
    pass

class CatalogueUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    pdf: Optional[bytes] = None  # For file updates; handled in controller

class CatalogueResponse(CatalogueBase):
    id: int
    pdf_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # Explicit for response if needed

class CatalogueDeleteResponse(BaseModel):
    message: str
    id: int

    model_config = ConfigDict(from_attributes=True)  # If using ORM in delete (optional)