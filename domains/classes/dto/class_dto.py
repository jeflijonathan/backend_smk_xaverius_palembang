from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MajorSimpleResponse(BaseModel):
    id_major: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class ClassGuardianSimpleResponse(BaseModel):
    id: str
    first_name: str
    last_name: Optional[str] = None
    niy: Optional[str] = None

    class Config:
        from_attributes = True


class SchoolInformationSimpleResponse(BaseModel):
    id_school_information: str
    name_school: Optional[str] = None
    periode: Optional[str] = None

    class Config:
        from_attributes = True


class StudentSimpleResponse(BaseModel):
    id: str
    nis: str
    nisn: str
    first_name: str
    last_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_url: Optional[str] = None
    status: Optional[bool] = True
    current_class: Optional[dict] = None

    class Config:
        from_attributes = True


class AddStudentsToClassDTO(BaseModel):
    student_ids: List[str]
    force_transfer: Optional[bool] = False


class ClassBase(BaseModel):
    id_major: str
    id_class_guardian: Optional[str] = None
    kelas: Optional[str] = None
    name: Optional[str] = None
    id_school_information: Optional[str] = None
    status: Optional[bool] = True


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    id_major: Optional[str] = None
    id_class_guardian: Optional[str] = None
    kelas: Optional[str] = None
    name: Optional[str] = None
    id_school_information: Optional[str] = None
    status: Optional[bool] = None


class ClassResponse(ClassBase):
    id_class: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    major: Optional[MajorSimpleResponse] = None
    class_guardian: Optional[ClassGuardianSimpleResponse] = None
    school_information: Optional[SchoolInformationSimpleResponse] = None
    students: Optional[List[StudentSimpleResponse]] = []
    total_students: Optional[int] = 0

    class Config:
        from_attributes = True

