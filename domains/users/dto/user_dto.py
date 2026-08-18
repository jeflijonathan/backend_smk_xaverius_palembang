from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from common.consts.user_role import UserRoles
from common.utils.validate_phone_number import validate_international_phone
from datetime import datetime


class CreateUserDTO(BaseModel):
    full_name: str = Field(
        ..., min_length=2, max_length=120, description="Nama lengkap pengguna"
    )
    username: str = Field(..., min_length=4, max_length=100, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
    nomor_telepon: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    roles: List[UserRoles] = Field(default=[UserRoles.USER])

    @field_validator("nomor_telepon")
    @classmethod
    def phone_validator(cls, value: Optional[str]) -> Optional[str]:
        return validate_international_phone(value)


class UpdateUserDTO(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=120)
    username: Optional[str] = Field(
        None, min_length=4, max_length=100, pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    nomor_telepon: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    status: Optional[bool] = None
    roles: Optional[List[UserRoles]] = None
    deleted_at: Optional[datetime] = None

    @field_validator("nomor_telepon")
    @classmethod
    def phone_validator(cls, value: Optional[str]) -> Optional[str]:
        return validate_international_phone(value)
