from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# CategoryScheduleTime DTOs
class CategoryScheduleTimeBase(BaseModel):
    name: str
    status: Optional[bool] = True


class CategoryScheduleTimeCreate(CategoryScheduleTimeBase):
    pass


class CategoryScheduleTimeUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class CategoryScheduleTimeResponse(CategoryScheduleTimeBase):
    id_category_schendule_time: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ScheduleTime DTOs
class ScheduleTimeBase(BaseModel):
    hari: str
    jam_awal: str
    jam_akhir: str
    id_category_schendule_time: str


class ScheduleTimeCreate(ScheduleTimeBase):
    pass


class ScheduleTimeUpdate(BaseModel):
    hari: Optional[str] = None
    jam_awal: Optional[str] = None
    jam_akhir: Optional[str] = None
    id_category_schendule_time: Optional[str] = None


class ScheduleTimeResponse(ScheduleTimeBase):
    id_schendule_time: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schedule DTOs
class ScheduleBase(BaseModel):
    id_category_subject: str
    id_duty_teacher: Optional[str] = None
    id_class: str
    id_schendule_time: str
    status: Optional[bool] = True


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    id_category_subject: Optional[str] = None
    id_duty_teacher: Optional[str] = None
    id_class: Optional[str] = None
    id_schendule_time: Optional[str] = None
    status: Optional[bool] = None


class ScheduleResponse(ScheduleBase):
    id_schendule: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
