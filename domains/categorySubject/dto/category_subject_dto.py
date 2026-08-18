from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategorySubjectCreate(BaseModel):
    name: str
    status: bool = True


class CategorySubjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class CategorySubjectResponse(BaseModel):
    id: str
    name: str
    status: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
