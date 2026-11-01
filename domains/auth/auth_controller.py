from fastapi import Depends, Request, Response, status
from sqlalchemy.orm import Session
from typing import Optional
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.auth.auth_service import AuthService, create_access_token
from domains.auth.dto.auth_dto import (
    EmployeeLoginRequest,
    StudentLoginRequest,
    RefreshTokenRequest,
    SelectRoleRequest,
    AuthResponseData,
    ProfileUpdateRequest,
)
from domains.auth.auth_middleware import get_current_user_payload
from domains.users.user_model import UserModel
from sqlalchemy.orm import joinedload


class AuthController(BaseController, prefix="/auth", tags=["Authentication"]):
    _service = AuthService()

    @classmethod
    def register_routes(cls):
        @cls.router.post("/employee/login", status_code=status.HTTP_200_OK)
        def login_employee(
            data: EmployeeLoginRequest,
            response: Response,
            db: Session = Depends(get_db),
        ):
            try:
                auth_data = cls._service.login_employee(db, data.niy, data.password)

                # Set cookies for access token and refresh token
                response.set_cookie(
                    key="access_token",
                    value=auth_data.access_token,
                    max_age=auth_data.expires_in,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )
                response.set_cookie(
                    key="refresh_token",
                    value=auth_data.refresh_token,
                    max_age=7 * 24 * 3600,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )

                return cls.handle_success(
                    data=auth_data.model_dump(),
                    message="Login pegawai berhasil",
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/student/login", status_code=status.HTTP_200_OK)
        def login_student(
            data: StudentLoginRequest,
            response: Response,
            db: Session = Depends(get_db),
        ):
            try:
                auth_data = cls._service.login_student(db, data.nis, data.password)

                # Set cookies for access token and refresh token
                response.set_cookie(
                    key="access_token",
                    value=auth_data.access_token,
                    max_age=auth_data.expires_in,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )
                response.set_cookie(
                    key="refresh_token",
                    value=auth_data.refresh_token,
                    max_age=7 * 24 * 3600,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )

                return cls.handle_success(
                    data=auth_data.model_dump(),
                    message="Login siswa berhasil",
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/refresh", status_code=status.HTTP_200_OK)
        def refresh_token(
            request: Request,
            response: Response,
            body: Optional[RefreshTokenRequest] = None,
            db: Session = Depends(get_db),
        ):
            try:
                rf_token = None
                if body and body.refresh_token:
                    rf_token = body.refresh_token
                elif request.cookies.get("refresh_token"):
                    rf_token = request.cookies.get("refresh_token")

                if not rf_token:
                    cls.handle_error(
                        detail="Refresh token tidak ditemukan di cookie maupun request body.",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )

                auth_data = cls._service.refresh_access_token(db, rf_token)

                response.set_cookie(
                    key="access_token",
                    value=auth_data.access_token,
                    max_age=auth_data.expires_in,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )

                return cls.handle_success(
                    data=auth_data.model_dump(),
                    message="Token berhasil diperbarui",
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_401_UNAUTHORIZED)
            except Exception as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        @cls.router.post("/logout", status_code=status.HTTP_200_OK)
        def logout(
            request: Request,
            response: Response,
            body: Optional[RefreshTokenRequest] = None,
            db: Session = Depends(get_db),
        ):
            try:
                rf_token = None
                if body and body.refresh_token:
                    rf_token = body.refresh_token
                elif request.cookies.get("refresh_token"):
                    rf_token = request.cookies.get("refresh_token")

                if rf_token:
                    cls._service.revoke_token(db, rf_token)

                # Clear cookies
                response.delete_cookie(key="access_token", path="/")
                response.delete_cookie(key="refresh_token", path="/")
                response.delete_cookie(key="active_role", path="/")

                return cls.handle_success(
                    data={"revoked": True},
                    message="Logout berhasil, token telah dicabut (revoked)",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/me", status_code=status.HTTP_200_OK)
        def get_me(
            payload: dict = Depends(get_current_user_payload),
            db: Session = Depends(get_db),
        ):
            try:
                user_id = payload.get("sub")
                active_role = payload.get("active_role")
                user_dto = cls._service.get_me(db, user_id, active_role)
                return cls.handle_success(
                    data=user_dto.model_dump(),
                    message="Data profil berhasil dimuat",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/profile", status_code=status.HTTP_200_OK)
        def get_profile(
            payload: dict = Depends(get_current_user_payload),
            db: Session = Depends(get_db),
        ):
            try:
                user_id = payload.get("sub")
                profile = cls._service.get_profile(db, user_id)
                return cls.handle_success(
                    data=profile.model_dump(),
                    message="Data profil berhasil dimuat",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/profile", status_code=status.HTTP_200_OK)
        def update_profile(
            data: ProfileUpdateRequest,
            payload: dict = Depends(get_current_user_payload),
            db: Session = Depends(get_db),
        ):
            try:
                user_id = payload.get("sub")
                updated_profile = cls._service.update_profile(db, user_id, data)
                return cls.handle_success(
                    data=updated_profile.model_dump(),
                    message="Profil berhasil diperbarui",
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/select-role", status_code=status.HTTP_200_OK)
        def select_role(
            data: SelectRoleRequest,
            response: Response,
            payload: dict = Depends(get_current_user_payload),
            db: Session = Depends(get_db),
        ):
            try:
                user_id = payload.get("sub")
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
                    cls.handle_error(detail="User tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)

                # Verify user possesses the chosen role
                role_names = [r.name.lower() for r in user.roles]
                chosen_role = data.role_name.strip().lower()
                if chosen_role not in role_names:
                    cls.handle_error(
                        detail=f"Role '{data.role_name}' tidak dimiliki oleh akun ini.",
                        status_code=status.HTTP_403_FORBIDDEN,
                    )

                # Find canonical role name
                canonical_role = next(
                    (r.name for r in user.roles if r.name.lower() == chosen_role),
                    data.role_name,
                )

                user_type = "employee" if user.employee_profile else ("student" if user.student_profile else "user")
                identifier = (
                    user.employee_profile.niy
                    if user.employee_profile
                    else (user.student_profile.nis if user.student_profile else user.username)
                )

                # Generate new access token with active_role encoded
                new_token, expires_in = create_access_token(
                    user=user,
                    user_type=user_type,
                    identifier=identifier,
                    active_role=canonical_role,
                )

                # Update cookies
                response.set_cookie(
                    key="access_token",
                    value=new_token,
                    max_age=expires_in,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )
                response.set_cookie(
                    key="active_role",
                    value=canonical_role,
                    max_age=7 * 24 * 3600,
                    httponly=False,
                    samesite="lax",
                    path="/",
                )

                profile_url = (
                    user.employee_profile.profile_url
                    if user.employee_profile
                    else (user.student_profile.profile_url if user.student_profile else None)
                )

                return cls.handle_success(
                    data={
                        "access_token": new_token,
                        "active_role": canonical_role,
                        "user": {
                            "id": user.id,
                            "full_name": user.full_name,
                            "username": user.username,
                            "user_type": user_type,
                            "identifier": identifier,
                            "active_role": canonical_role,
                            "roles": [{"id": r.id, "name": r.name} for r in user.roles],
                            "profile_url": profile_url,
                        },
                    },
                    message=f"Role aktif berhasil diatur ke '{canonical_role}'",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


AuthController.register_routes()
router = AuthController.get_router()

