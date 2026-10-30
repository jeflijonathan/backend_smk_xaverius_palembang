import phonenumbers
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Any
from datetime import date, datetime


def normalize_phone_number(v: Optional[str]) -> Optional[str]:
    if not v or not str(v).strip():
        return None
    v_clean = str(v).strip()
    try:
        parsed = phonenumbers.parse(v_clean, "ID")
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Nomor telepon tidak valid untuk wilayah Indonesia")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        raise ValueError("Format nomor telepon tidak valid (contoh: 081234567890 atau +6281234567890)")


class RoleResponseDTO(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class CreateParentDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    nik: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    occupation: Optional[str] = Field(None, max_length=100)
    income: Optional[str] = Field(None, max_length=50)

    @field_validator("phone_number", mode="before")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        return normalize_phone_number(v)


class ParentResponseDTO(BaseModel):
    id: str
    name: str
    nik: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateStudentDTO(BaseModel):
    # Auth user
    username: Optional[str] = Field(None, min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=255)
    role_ids: Optional[List[str]] = None

    # Student Profile
    nis: str = Field(..., min_length=1, max_length=100)
    nisn: str = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field("L", max_length=1)
    birth_place: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    address: Optional[str] = Field(None, max_length=100)
    rt: Optional[str] = Field(None, max_length=10)
    rw: Optional[str] = Field(None, max_length=10)
    zip_code: Optional[str] = Field(None, max_length=5)
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_url: Optional[str] = None
    description: Optional[str] = None
    status: bool = True

    # Data Orang Tua / Parent
    parent: Optional[CreateParentDTO] = None
    mother: Optional[CreateParentDTO] = None
    parents: Optional[List[CreateParentDTO]] = None

    # Flattened parent fields for frontend convenience
    parent_name: Optional[str] = None
    parent_nik: Optional[str] = None
    parent_phone_number: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    parent_occupation: Optional[str] = None
    parent_income: Optional[str] = None

    mother_name: Optional[str] = None
    mother_nik: Optional[str] = None
    mother_phone_number: Optional[str] = None
    mother_email: Optional[EmailStr] = None
    mother_occupation: Optional[str] = None
    mother_income: Optional[str] = None

    @field_validator("phone_number", "parent_phone_number", "mother_phone_number", mode="before")
    @classmethod
    def validate_phones(cls, v: Optional[str]) -> Optional[str]:
        return normalize_phone_number(v)


class UpdateStudentDTO(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    role_ids: Optional[List[str]] = None

    nis: Optional[str] = Field(None, min_length=1, max_length=100)
    nisn: Optional[str] = Field(None, min_length=1, max_length=100)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, max_length=1)
    birth_place: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    address: Optional[str] = Field(None, max_length=100)
    rt: Optional[str] = Field(None, max_length=10)
    rw: Optional[str] = Field(None, max_length=10)
    zip_code: Optional[str] = Field(None, max_length=5)
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None

    parent: Optional[CreateParentDTO] = None
    mother: Optional[CreateParentDTO] = None
    parents: Optional[List[CreateParentDTO]] = None

    parent_name: Optional[str] = None
    parent_nik: Optional[str] = None
    parent_phone_number: Optional[str] = None
    parent_email: Optional[EmailStr] = None
    parent_occupation: Optional[str] = None
    parent_income: Optional[str] = None

    mother_name: Optional[str] = None
    mother_nik: Optional[str] = None
    mother_phone_number: Optional[str] = None
    mother_email: Optional[EmailStr] = None
    mother_occupation: Optional[str] = None
    mother_income: Optional[str] = None

    @field_validator("phone_number", "parent_phone_number", "mother_phone_number", mode="before")
    @classmethod
    def validate_phones(cls, v: Optional[str]) -> Optional[str]:
        return normalize_phone_number(v)


class UserStudentResponseDTO(BaseModel):
    id: str
    username: str
    full_name: str
    roles: Optional[List[RoleResponseDTO]] = []

    class Config:
        from_attributes = True


class StudentResponseDTO(BaseModel):
    id: str
    user_id: str
    nis: str
    nisn: str
    first_name: str
    last_name: str
    gender: Optional[str] = "L"
    rt: Optional[str] = None
    rw: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[date] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    profile_url: Optional[str] = None
    status: bool = True
    user: Optional[UserStudentResponseDTO] = None
    roles: Optional[List[RoleResponseDTO]] = []
    role_ids: Optional[List[str]] = []
    parents: Optional[List[ParentResponseDTO]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_student(cls, student: Any):
        dto = cls.model_validate(student)
        if hasattr(student, "user") and student.user:
            user_roles = getattr(student.user, "roles", []) or []
            dto.roles = [RoleResponseDTO.model_validate(r) for r in user_roles]
            dto.role_ids = [r.id for r in user_roles]
        return dto
