from typing import Optional
from pydantic import BaseModel, ConfigDict, constr

class SubCategoryCreate(BaseModel):
    catname: str
    subcatname: str
    slug: str

class  SubCategoryResponse(BaseModel):
    id: int
    catname: Optional[str] = None
    slug: Optional[str] = None
    slug: Optional[str] = None

class SubCategoryUpdate(BaseModel):
    catname: str
    subcatname: str
    slug: str

model_config = ConfigDict(from_attributes=True)
