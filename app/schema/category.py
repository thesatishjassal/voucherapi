from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class CategoryCreate(BaseModel):
    name: str
    slug: str

class  CategoryResponse(BaseModel):
    id: int
    name: Optional[str] = None
    slug: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: str
    slug: str


model_config = ConfigDict(from_attributes=True)
