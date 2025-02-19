from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class CategoryCreate(BaseModel):
    catname: str
    slug: str

class  CategoryResponse(BaseModel):
    id: int
    catname: Optional[str] = None
    slug: Optional[str] = None

class CategoryUpdate(BaseModel):
    catname: str
    slug: str


model_config = ConfigDict(from_attributes=True)
