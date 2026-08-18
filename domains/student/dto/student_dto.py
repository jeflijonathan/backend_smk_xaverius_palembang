from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CreateStudentDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=255)
    nis: str = Field(..., min_length=1, max_length=100)
    nisn: str = Field(..., min_length=1, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    status: bool = True

class UpdateStudentDTO(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    nis: Optional[str] = Field(None, min_length=1, max_length=100)
    nisn: Optional[str] = Field(None, min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    status: Optional[bool] = None
