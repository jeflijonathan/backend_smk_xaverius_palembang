from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MajorBase(BaseModel):
    name: str
    status: Optional[bool] = True


class MajorCreate(MajorBase):
    pass


class MajorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None


class MajorResponse(MajorBase):
    id_major: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
