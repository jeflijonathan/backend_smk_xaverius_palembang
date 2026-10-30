from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SchoolSubjectBase(BaseModel):
    name: str
    id_category_subject: Optional[str] = None
    category_subject_id: Optional[str] = None
    id_major: Optional[str] = None
    code_subject: Optional[str] = None
    kelas: Optional[str] = None
    fase: Optional[str] = None
    status: Optional[bool] = True

    def get_category_subject_id(self) -> str:
        return self.id_category_subject or self.category_subject_id or ""


class SchoolSubjectCreate(SchoolSubjectBase):
    pass


class SchoolSubjectUpdate(BaseModel):
    name: Optional[str] = None
    id_category_subject: Optional[str] = None
    category_subject_id: Optional[str] = None
    id_major: Optional[str] = None
    code_subject: Optional[str] = None
    kelas: Optional[str] = None
    fase: Optional[str] = None
    status: Optional[bool] = None


class CategorySimpleResponse(BaseModel):
    id_category_subject: Optional[str] = None
    id: Optional[str] = None
    name: str

    class Config:
        from_attributes = True


class MajorSimpleResponse(BaseModel):
    id_major: Optional[str] = None
    id: Optional[str] = None
    name: str

    class Config:
        from_attributes = True


class SchoolSubjectResponse(BaseModel):
    id_subject: Optional[str] = None
    id: Optional[str] = None
    name: str
    id_category_subject: Optional[str] = None
    id_major: Optional[str] = None
    code_subject: Optional[str] = None
    kelas: Optional[str] = None
    fase: Optional[str] = None
    status: bool = True
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    category: Optional[CategorySimpleResponse] = None
    major: Optional[MajorSimpleResponse] = None

    class Config:
        from_attributes = True
