from pydantic import BaseModel
from typing import List, Dict, Any

class CSVResponse(BaseModel):
    filename: str
    rows: int
    data: List[Dict[str, Any]]
