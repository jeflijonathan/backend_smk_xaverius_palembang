from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SchoolInformationBase(BaseModel):
    name_school: str
    periode: Optional[str] = None
    NPSN: Optional[str] = None
    id_headmaster: Optional[str] = None
    alamat: Optional[str] = None
    status: Optional[bool] = True


class SchoolInformationCreate(SchoolInformationBase):
    pass


class SchoolInformationUpdate(BaseModel):
    name_school: Optional[str] = None
    periode: Optional[str] = None
    NPSN: Optional[str] = None
    id_headmaster: Optional[str] = None
    alamat: Optional[str] = None
    status: Optional[bool] = None


class SchoolInformationResponse(SchoolInformationBase):
    id_school_information: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
