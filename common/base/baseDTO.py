from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BaseDTO(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
