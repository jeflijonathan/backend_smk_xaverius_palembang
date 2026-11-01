from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from config.env.env import env
from domains.users.user_model import UserModel
from domains.employee.employee_model import EmployeeModel, EmployeeDetailModel
from domains.student.student_model import StudentModel
from domains.auth.refresh_token_model import RefreshTokenModel
from domains.auth.dto.auth_dto import (
    AuthResponseData,
    AuthUserDTO,
    RoleDTO,
    ProfileDetailDTO,
    ProfileResponseDTO,
    ProfileUpdateRequest,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_or_plain: str) -> bool:
    if not hashed_or_plain:
        return False
    if hashed_or_plain.startswith("$2"):
        try:
            return pwd_context.verify(plain_password, hashed_or_plain)
        except Exception:
            return False
    # Fallback to direct plaintext comparison
    return plain_password == hashed_or_plain


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    user: UserModel,
    user_type: str,
    identifier: str,
    active_role: Optional[str] = None
) -> tuple[str, int]:
    expire_delta = timedelta(minutes=env.accessTokenExpireMinutes)
    now = datetime.now(timezone.utc)
    expire = now + expire_delta
    payload = {
        "sub": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "user_type": user_type,
        "identifier": identifier,
        "roles": [r.name for r in user.roles],
        "active_role": active_role,
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, env.jwtSecret, algorithm=env.jwtAlgorithm)
    expires_in = int(expire_delta.total_seconds())
    return token, expires_in


def create_refresh_token(user_id: str) -> tuple[str, datetime]:
    expire_delta = timedelta(days=env.refreshTokenExpireDays)
    now = datetime.now(timezone.utc)
    expire = now + expire_delta
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, env.jwtSecret, algorithm=env.jwtAlgorithm)
    return token, expire.replace(tzinfo=None)


class AuthService:
    def revoke_expired_tokens(self, db: Session):
        now = datetime.utcnow()
        db.query(RefreshTokenModel).filter(
            RefreshTokenModel.expires_at < now,
            RefreshTokenModel.is_revoked == False
        ).update({"is_revoked": True})
        db.commit()

    def login_employee(self, db: Session, niy: str, password: str) -> AuthResponseData:
        self.revoke_expired_tokens(db)
        emp = (
            db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.user).joinedload(UserModel.roles))
            .filter(
                EmployeeModel.niy == niy.strip(),
                EmployeeModel.deleted_at.is_(None),
                EmployeeModel.status == True,
            )
            .first()
        )

        if not emp or not emp.user:
            raise ValueError("NIY atau password salah")

        if not emp.user.status:
            raise ValueError("Akun pegawai dinonaktifkan")

        if not verify_password(password, emp.user.password):
            raise ValueError("NIY atau password salah")

        access_token, expires_in = create_access_token(
            user=emp.user,
            user_type="employee",
            identifier=emp.niy,
        )
        refresh_token_str, refresh_expires_at = create_refresh_token(emp.user.id)

        # Save refresh token in database
        rf_record = RefreshTokenModel(
            user_id=emp.user.id,
            token=refresh_token_str,
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        db.add(rf_record)
        db.commit()

        return AuthResponseData(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="Bearer",
            expires_in=expires_in,
            user=AuthUserDTO(
                id=emp.user.id,
                full_name=emp.user.full_name or f"{emp.first_name} {emp.last_name or ''}".strip(),
                username=emp.user.username,
                user_type="employee",
                identifier=emp.niy,
                roles=[RoleDTO(id=r.id, name=r.name) for r in emp.user.roles],
                profile_url=emp.profile_url,
            ),
        )

    def login_student(self, db: Session, nis: str, password: str) -> AuthResponseData:
        self.revoke_expired_tokens(db)
        student = (
            db.query(StudentModel)
            .options(joinedload(StudentModel.user).joinedload(UserModel.roles))
            .filter(
                StudentModel.nis == nis.strip(),
                StudentModel.deleted_at.is_(None),
                StudentModel.status == True,
            )
            .first()
        )

        if not student or not student.user:
            raise ValueError("NIS atau password salah")

        if not student.user.status:
            raise ValueError("Akun siswa dinonaktifkan")

        if not verify_password(password, student.user.password):
            raise ValueError("NIS atau password salah")

        access_token, expires_in = create_access_token(
            user=student.user,
            user_type="student",
            identifier=student.nis,
        )
        refresh_token_str, refresh_expires_at = create_refresh_token(student.user.id)

        # Save refresh token in database
        rf_record = RefreshTokenModel(
            user_id=student.user.id,
            token=refresh_token_str,
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        db.add(rf_record)
        db.commit()

        return AuthResponseData(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="Bearer",
            expires_in=expires_in,
            user=AuthUserDTO(
                id=student.user.id,
                full_name=student.user.full_name or f"{student.first_name} {student.last_name or ''}".strip(),
                username=student.user.username,
                user_type="student",
                identifier=student.nis,
                roles=[RoleDTO(id=r.id, name=r.name) for r in student.user.roles],
                profile_url=student.profile_url,
            ),
        )

    def refresh_access_token(self, db: Session, token: str) -> AuthResponseData:
        if not token:
            raise ValueError("Refresh token tidak disediakan")

        record = (
            db.query(RefreshTokenModel)
            .filter(RefreshTokenModel.token == token)
            .first()
        )

        if not record:
            raise ValueError("Refresh token tidak valid atau tidak ditemukan")

        if record.is_revoked:
            raise ValueError("Refresh token telah dicabut (revoked)")

        if record.expires_at < datetime.utcnow():
            record.is_revoked = True
            db.commit()
            raise ValueError("Refresh token telah kedaluwarsa dan otomatis dicabut")

        try:
            payload = jwt.decode(token, env.jwtSecret, algorithms=[env.jwtAlgorithm])
            if payload.get("type") != "refresh":
                raise ValueError("Format token bukan refresh token")
        except jwt.ExpiredSignatureError:
            record.is_revoked = True
            db.commit()
            raise ValueError("Refresh token telah kedaluwarsa")
        except Exception:
            raise ValueError("Tanda tangan refresh token tidak valid")

        user = (
            db.query(UserModel)
            .options(
                joinedload(UserModel.roles),
                joinedload(UserModel.employee_profile),
                joinedload(UserModel.student_profile),
            )
            .filter(UserModel.id == record.user_id, UserModel.status == True)
            .first()
        )

        if not user:
            raise ValueError("Pengguna tidak ditemukan atau berstatus tidak aktif")

        user_type = "employee" if user.employee_profile else ("student" if user.student_profile else "user")
        identifier = (
            user.employee_profile.niy
            if user.employee_profile
            else (user.student_profile.nis if user.student_profile else user.username)
        )
        profile_url = (
            user.employee_profile.profile_url
            if user.employee_profile
            else (user.student_profile.profile_url if user.student_profile else None)
        )

        new_access_token, expires_in = create_access_token(
            user=user,
            user_type=user_type,
            identifier=identifier,
        )

        return AuthResponseData(
            access_token=new_access_token,
            refresh_token=token,
            token_type="Bearer",
            expires_in=expires_in,
            user=AuthUserDTO(
                id=user.id,
                full_name=user.full_name,
                username=user.username,
                user_type=user_type,
                identifier=identifier,
                roles=[RoleDTO(id=r.id, name=r.name) for r in user.roles],
                profile_url=profile_url,
            ),
        )

    def revoke_token(self, db: Session, token: str) -> bool:
        if not token:
            return False
        record = (
            db.query(RefreshTokenModel)
            .filter(RefreshTokenModel.token == token)
            .first()
        )
        if record:
            record.is_revoked = True
            db.commit()
            return True
        return False

    def get_me(self, db: Session, user_id: str, active_role: Optional[str] = None) -> AuthUserDTO:
        user = (
            db.query(UserModel)
            .options(
                joinedload(UserModel.roles),
                joinedload(UserModel.employee_profile),
                joinedload(UserModel.student_profile),
            )
            .filter(UserModel.id == user_id, UserModel.status == True)
            .first()
        )

        if not user:
            raise ValueError("Pengguna tidak ditemukan")

        user_type = "employee" if user.employee_profile else ("student" if user.student_profile else "user")
        identifier = (
            user.employee_profile.niy
            if user.employee_profile
            else (user.student_profile.nis if user.student_profile else user.username)
        )
        profile_url = (
            user.employee_profile.profile_url
            if user.employee_profile
            else (user.student_profile.profile_url if user.student_profile else None)
        )

        return AuthUserDTO(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
            user_type=user_type,
            identifier=identifier,
            roles=[RoleDTO(id=r.id, name=r.name) for r in user.roles],
            profile_url=profile_url,
            active_role=active_role,
        )

    def get_profile(self, db: Session, user_id: str) -> ProfileResponseDTO:
        user = (
            db.query(UserModel)
            .options(
                joinedload(UserModel.roles),
                joinedload(UserModel.employee_profile).joinedload(EmployeeModel.detail),
                joinedload(UserModel.student_profile),
            )
            .filter(UserModel.id == user_id, UserModel.status == True)
            .first()
        )

        if not user:
            raise ValueError("Pengguna tidak ditemukan")

        user_type = "employee" if user.employee_profile else ("student" if user.student_profile else "user")
        roles = [RoleDTO(id=r.id, name=r.name) for r in user.roles]

        if user.employee_profile:
            emp = user.employee_profile
            detail_dto = None
            if emp.detail:
                detail_dto = ProfileDetailDTO(
                    gender=emp.detail.gender,
                    birth_place=emp.detail.birth_place,
                    birth_date=str(emp.detail.birth_date) if emp.detail.birth_date else None,
                    address=emp.detail.address,
                    RT=emp.detail.RT,
                    RW=emp.detail.RW,
                    zip_code=emp.detail.zip_code,
                    phone_number=emp.detail.phone_number,
                    description=emp.detail.description,
                )
            return ProfileResponseDTO(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                first_name=emp.first_name,
                last_name=emp.last_name,
                user_type="employee",
                identifier=emp.niy,
                email=emp.email,
                profile_url=emp.profile_url,
                status=emp.status,
                roles=roles,
                detail=detail_dto,
            )
        elif user.student_profile:
            std = user.student_profile
            detail_dto = ProfileDetailDTO(
                gender=std.gender,
                birth_place=std.birth_place,
                birth_date=str(std.birth_date) if std.birth_date else None,
                address=std.address,
                RT=std.rt,
                RW=std.rw,
                zip_code=std.zip_code,
                phone_number=std.phone_number,
                description=None,
            )
            return ProfileResponseDTO(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                first_name=std.first_name,
                last_name=std.last_name,
                user_type="student",
                identifier=std.nis,
                nisn=std.nisn,
                email=std.email,
                profile_url=std.profile_url,
                status=std.status,
                roles=roles,
                detail=detail_dto,
            )
        else:
            return ProfileResponseDTO(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                first_name=user.full_name,
                last_name=None,
                user_type="user",
                identifier=user.username,
                email=None,
                profile_url=None,
                status=user.status,
                roles=roles,
                detail=None,
            )

    def update_profile(self, db: Session, user_id: str, data: ProfileUpdateRequest) -> ProfileResponseDTO:
        user = (
            db.query(UserModel)
            .options(
                joinedload(UserModel.roles),
                joinedload(UserModel.employee_profile).joinedload(EmployeeModel.detail),
                joinedload(UserModel.student_profile),
            )
            .filter(UserModel.id == user_id, UserModel.status == True)
            .first()
        )

        if not user:
            raise ValueError("Pengguna tidak ditemukan")

        # 1. Update Password jika diisi
        if data.password and data.password.strip():
            pwd = data.password.strip()
            if len(pwd) < 6:
                raise ValueError("Password baru minimal 6 karakter")
            user.password = hash_password(pwd)

        # Helper parse tanggal lahir
        parsed_birth_date = None
        if data.birth_date and data.birth_date.strip():
            from datetime import date
            try:
                parsed_birth_date = date.fromisoformat(data.birth_date.strip())
            except ValueError:
                pass

        # 2. Update Employee Profile
        if user.employee_profile:
            emp = user.employee_profile
            if data.email is not None and data.email.strip():
                new_email = data.email.strip()
                existing_email = db.query(EmployeeModel).filter(
                    EmployeeModel.email == new_email,
                    EmployeeModel.id != emp.id,
                    EmployeeModel.deleted_at == None,
                ).first()
                if existing_email:
                    raise ValueError(f"Email '{new_email}' sudah digunakan oleh pengguna lain")
                emp.email = new_email

            if data.profile_url is not None:
                emp.profile_url = data.profile_url if data.profile_url.strip() else None

            if not emp.detail:
                emp.detail = EmployeeDetailModel(employee_id=emp.id)
                db.add(emp.detail)

            if data.gender is not None:
                emp.detail.gender = data.gender if data.gender in ["L", "P"] else None
            if data.birth_place is not None:
                emp.detail.birth_place = data.birth_place.strip() if data.birth_place.strip() else None
            if data.birth_date is not None:
                emp.detail.birth_date = parsed_birth_date
            if data.address is not None:
                emp.detail.address = data.address.strip() if data.address.strip() else None
            if data.RT is not None:
                emp.detail.RT = data.RT.strip() if data.RT.strip() else None
            if data.RW is not None:
                emp.detail.RW = data.RW.strip() if data.RW.strip() else None
            if data.zip_code is not None:
                emp.detail.zip_code = data.zip_code.strip() if data.zip_code.strip() else None
            if data.phone_number is not None:
                emp.detail.phone_number = data.phone_number.strip() if data.phone_number.strip() else None
            if data.description is not None:
                emp.detail.description = data.description.strip() if data.description.strip() else None

        # 3. Update Student Profile
        elif user.student_profile:
            std = user.student_profile
            if data.email is not None and data.email.strip():
                new_email = data.email.strip()
                existing_email = db.query(StudentModel).filter(
                    StudentModel.email == new_email,
                    StudentModel.id != std.id,
                    StudentModel.deleted_at == None,
                ).first()
                if existing_email:
                    raise ValueError(f"Email '{new_email}' sudah digunakan oleh siswa lain")
                std.email = new_email

            if data.profile_url is not None:
                std.profile_url = data.profile_url if data.profile_url.strip() else None

            if data.gender is not None:
                std.gender = data.gender if data.gender in ["L", "P"] else std.gender
            if data.birth_place is not None:
                std.birth_place = data.birth_place.strip() if data.birth_place.strip() else None
            if data.birth_date is not None:
                std.birth_date = parsed_birth_date
            if data.address is not None:
                std.address = data.address.strip() if data.address.strip() else None
            if data.RT is not None:
                std.rt = data.RT.strip() if data.RT.strip() else None
            if data.RW is not None:
                std.rw = data.RW.strip() if data.RW.strip() else None
            if data.zip_code is not None:
                std.zip_code = data.zip_code.strip() if data.zip_code.strip() else None
            if data.phone_number is not None:
                std.phone_number = data.phone_number.strip() if data.phone_number.strip() else None

        db.commit()
        return self.get_profile(db, user_id)

