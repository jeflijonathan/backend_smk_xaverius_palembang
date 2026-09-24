from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClassBase(BaseModel):
    id_major: str
    id_class_guardian: Optional[str] = None
    name: str
    status: Optional[bool] = True


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    id_major: Optional[str] = None
    id_class_guardian: Optional[str] = None
    name: Optional[str] = None
    status: Optional[bool] = None


class ClassResponse(ClassBase):
    id_class: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
