from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TeacherSubjectBase(BaseModel):
    id_category_subject: str
    id_subject: str
    id_teacher: str
    jp_amount: Optional[int] = 0
    status: Optional[bool] = True


class TeacherSubjectCreate(TeacherSubjectBase):
    pass


class TeacherSubjectUpdate(BaseModel):
    id_category_subject: Optional[str] = None
    id_subject: Optional[str] = None
    id_teacher: Optional[str] = None
    jp_amount: Optional[int] = None
    status: Optional[bool] = None


class TeacherSubjectResponse(TeacherSubjectBase):
    id_teacher_subject: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
