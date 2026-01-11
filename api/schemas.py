from pydantic import BaseModel
from typing import Optional, List, Any

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    photo_path: Optional[str] = None
    qr_hash: str

class StatusResponse(BaseModel):
    qr_hash: str
    is_confirmed: bool

class VectorUpdate(BaseModel):
    employee_id: int
    vector_features: List[float] 
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    qr_hash: Optional[str] = None
    photo_path: Optional[str] = None