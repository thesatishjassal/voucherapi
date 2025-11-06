from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CatalogueBase(BaseModel):
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None

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

    class Config:
        orm_mode = True

class CatalogueDeleteResponse(BaseModel):
    message: str
    id: int