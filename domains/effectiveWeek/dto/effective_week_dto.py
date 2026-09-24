from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EffectiveWeekBase(BaseModel):
    id_subject: str
    Alokasi_Intrakurikuler: Optional[int] = 0
    Alokasi_Kokurikuler: Optional[int] = 0


class EffectiveWeekCreate(EffectiveWeekBase):
    pass


class EffectiveWeekUpdate(BaseModel):
    id_subject: Optional[str] = None
    Alokasi_Intrakurikuler: Optional[int] = None
    Alokasi_Kokurikuler: Optional[int] = None


class EffectiveWeekResponse(EffectiveWeekBase):
    id_effective_week: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
