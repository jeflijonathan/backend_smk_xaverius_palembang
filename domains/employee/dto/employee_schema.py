from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UserEmployeeBase(BaseModel):
    username: str

class UserEmployeeCreate(UserEmployeeBase):
    password: str

class EmployeeBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    profile_url: Optional[str] = None
    niy: str
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    email: EmailStr
    address: Optional[str] = None
    RT: Optional[str] = None
    RW: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
    status: bool = True

class EmployeeCreate(BaseModel):
    user: UserEmployeeCreate
    profile: EmployeeBase

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_url: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    RT: Optional[str] = None
    RW: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
