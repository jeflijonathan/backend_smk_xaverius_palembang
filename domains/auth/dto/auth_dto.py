from pydantic import BaseModel, Field
from typing import Optional, List


class EmployeeLoginRequest(BaseModel):
    niy: str = Field(..., description="Nomor Induk Yayasan (NIY) Pegawai/Guru")
    password: str = Field(..., description="Kata sandi akun")


class StudentLoginRequest(BaseModel):
    nis: str = Field(..., description="Nomor Induk Siswa (NIS)")
    password: str = Field(..., description="Kata sandi akun")


class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = Field(None, description="Refresh token string (opsional jika ada di cookie)")


class SelectRoleRequest(BaseModel):
    role_name: str = Field(..., description="Nama role yang dipilih pengguna")


class RoleDTO(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class AuthUserDTO(BaseModel):
    id: str
    full_name: str
    username: str
    user_type: str  # "employee" | "student"
    identifier: str  # NIY for employee, NIS for student
    roles: List[RoleDTO]
    profile_url: Optional[str] = None
    active_role: Optional[str] = None

    class Config:
        from_attributes = True


class AuthResponseData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int  # in seconds
    user: AuthUserDTO


class ProfileDetailDTO(BaseModel):
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    RT: Optional[str] = None
    RW: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None


class ProfileResponseDTO(BaseModel):
    user_id: str
    username: str
    full_name: str
    first_name: str
    last_name: Optional[str] = None
    user_type: str  # "employee" | "student"
    identifier: str  # NIY for employee, NIS for student
    nisn: Optional[str] = None
    email: Optional[str] = None
    profile_url: Optional[str] = None
    status: bool = True
    roles: List[RoleDTO]
    detail: Optional[ProfileDetailDTO] = None


class ProfileUpdateRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    profile_url: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    RT: Optional[str] = None
    RW: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
