from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategorySubjectBase(BaseModel):
    name: str

class CategorySubjectCreate(CategorySubjectBase):
    pass

class CategorySubjectUpdate(CategorySubjectBase):
    name: Optional[str] = None

class CategorySubjectResponse(CategorySubjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SchoolSubjectBase(BaseModel):
    name: str
    category_subject_id: str

class SchoolSubjectCreate(SchoolSubjectBase):
    pass

class SchoolSubjectUpdate(BaseModel):
    name: Optional[str] = None
    category_subject_id: Optional[str] = None

class SchoolSubjectResponse(SchoolSubjectBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
