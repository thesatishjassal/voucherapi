from pydantic import BaseModel
from datetime import datetime

class CatalogueBase(BaseModel):
    name: str
    category: str | None = None
    brand: str | None = None

class CatalogueCreate(CatalogueBase):
    pass

class CatalogueResponse(CatalogueBase):
    id: int
    pdf_url: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
