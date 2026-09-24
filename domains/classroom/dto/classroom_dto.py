from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClassroomBase(BaseModel):
    id_teacher_subject: str
    id_class: str
    id_school_information: str
    status: Optional[bool] = True


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomUpdate(BaseModel):
    id_teacher_subject: Optional[str] = None
    id_class: Optional[str] = None
    id_school_information: Optional[str] = None
    status: Optional[bool] = None


class ClassroomResponse(ClassroomBase):
    id_class_room: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
