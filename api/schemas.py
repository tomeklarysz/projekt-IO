from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    photo_path: Optional[str] = None
    qr_hash: str
    qr_expiration_date: Optional[date] = None
    qr_path: Optional[str] = None

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
    qr_expiration_date: Optional[date] = None

class ExpiryRequest(BaseModel):
    qr_hash: str
    new_expiry_date: date