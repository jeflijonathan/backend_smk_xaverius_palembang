import phonenumbers
from typing import Optional, List, Literal
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserEmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=3, description="Nama lengkap minimal 3 karakter")
    username: str = Field(..., min_length=3, pattern="^[a-zA-Z0-9_.-]+$", description="Username alfanumerik minimal 3 karakter")
    password: str = Field(..., min_length=6, description="Password minimal 6 karakter")

    @field_validator('username')
    @classmethod
    def username_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username tidak boleh kosong")
        return v.strip()

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: Optional[str] = None
    profile_url: Optional[str] = None
    niy: str = Field(..., min_length=3)
    email: EmailStr
    status: bool = True

    @field_validator('first_name')
    @classmethod
    def first_name_valid(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("First name tidak boleh kosong")
        return v.strip()

class EmployeeDetailBase(BaseModel):
    gender: Optional[Literal["L", "P"]] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    RT: Optional[str] = None
    RW: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None 
    description: Optional[str] = None

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v_clean = v.strip()
        try:
            parsed = phonenumbers.parse(v_clean, "ID")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Nomor telepon tidak valid untuk wilayah Indonesia")
            # Normalisasi ke format E.164: +62xxxxxxxx
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError("Format nomor telepon tidak valid (contoh: 081234567890 atau +6281234567890)")

    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    user: UserEmployeeCreate
    profile: EmployeeBase
    detail: Optional[EmployeeDetailBase] = None
    role_ids: Optional[List[str]] = None

class EmployeeUpdate(BaseModel):
    niy: Optional[str] = Field(None, min_length=3, max_length=100, description="NIY minimal 3 karakter")
    username: Optional[str] = Field(None, min_length=3, max_length=100, pattern="^[a-zA-Z0-9_.-]+$", description="Username alfanumerik minimal 3 karakter")
    email: Optional[EmailStr] = Field(None, description="Email tidak valid / kosong")
    password: Optional[str] = Field(None, min_length=6, description="Password minimal 6 karakter")
    first_name: Optional[str] = Field(None, min_length=1, max_length=255, description="First name tidak boleh kosong")
    last_name: Optional[str] = Field(None, max_length=255)
    profile_url: Optional[str] = None
    status: Optional[bool] = None
    detail: Optional[EmployeeDetailBase] = None
    role_ids: Optional[List[str]] = None

    @field_validator('niy')
    @classmethod
    def niy_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_stripped = v.strip()
            if not v_stripped:
                raise ValueError("NIY tidak boleh kosong")
            return v_stripped
        return v

    @field_validator('username')
    @classmethod
    def username_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_stripped = v.strip()
            if not v_stripped:
                raise ValueError("Username tidak boleh kosong")
            return v_stripped
        return v

    @field_validator('first_name')
    @classmethod
    def first_name_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_stripped = v.strip()
            if not v_stripped:
                raise ValueError("First name tidak boleh kosong")
            return v_stripped
        return v

    @field_validator('password')
    @classmethod
    def password_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_stripped = v.strip()
            if not v_stripped:
                return None
            if len(v_stripped) < 6:
                raise ValueError("Password minimal 6 karakter")
            return v_stripped
        return v

class RoleResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str
    roles: Optional[List[RoleResponse]] = None

    class Config:
        from_attributes = True

class EmployeeResponse(EmployeeBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    detail: Optional[EmployeeDetailBase] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True