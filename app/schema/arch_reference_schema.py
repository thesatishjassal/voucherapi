from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


# ── REQUEST SCHEMAS ──────────────────────────────────────────

class AddArchReferenceSchema(BaseModel):
    """Payload the salesperson sends to add an architect reference."""
    architect_id: int
    notes: Optional[str] = None


class UpdateArchReferenceSchema(BaseModel):
    """Payload to update the notes on an existing reference."""
    notes: Optional[str] = None


# ── RESPONSE SCHEMAS ─────────────────────────────────────────

class ArchitectBriefSchema(BaseModel):
    """Minimal architect info embedded inside a reference response."""
    id: int
    full_name: str
    email: str
    mobile_number: Optional[str] = None
    firm_name: Optional[str] = None
    profession: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True


class SalesPersonBriefSchema(BaseModel):
    """Minimal salesperson info embedded inside a reference response."""
    id: int
    full_name: str
    email: str
    mobile_number: Optional[str] = None

    class Config:
        from_attributes = True


class ArchReferenceResponseSchema(BaseModel):
    id: int
    sales_person_id: int
    architect_id: int
    notes: Optional[str] = None
    added_at: datetime
    architect: Optional[ArchitectBriefSchema] = None
    sales_person: Optional[SalesPersonBriefSchema] = None

    class Config:
        from_attributes = True
