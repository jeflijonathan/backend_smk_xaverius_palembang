from fastapi import Depends, status, Body
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from common.utils.file_location import move_temp_to_location
from domains.users.user_service import UserService
from domains.users.dto.user_dto import CreateUserDTO, UpdateUserDTO


class UserController(BaseController, prefix="/users", tags=["Users"]):
    _user_service = UserService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                users = cls._user_service.get_all_users(db)
                return cls.handle_success(
                    data=users, message="Users retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(user_data: CreateUserDTO, db: Session = Depends(get_db)):
            try:
                user = cls._user_service.create_user(db, user_data)
                return cls.handle_success(
                    data=user,
                    message="User created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.put("/{user_id}", status_code=status.HTTP_200_OK)
        def update_user(
            user_id: str, update_data: UpdateUserDTO, db: Session = Depends(get_db)
        ):
            try:
                user = cls._user_service.update_user(db, user_id, update_data)
                if not user:
                    cls.handle_error(
                        detail=f"User with id {user_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=user, message="User updated successfully"
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        # ──────────────────────────────────────────────
        # CONTOH: Menerapkan move_temp_to_location
        # ──────────────────────────────────────────────
        # Flow:
        #   1. Client upload file lewat  POST /api/upload/  → dapat temp_filename
        #   2. Client kirim temp_filename ke endpoint ini   → file dipindahkan ke uploads/users/avatars/
        #
        @cls.router.put("/{user_id}/avatar", status_code=status.HTTP_200_OK)
        def update_avatar(
            user_id: str,
            temp_filename: str = Body(..., embed=True,
                                      description="temp_filename dari response POST /api/upload/"),
            db: Session = Depends(get_db),
        ):
            """
            Contoh penggunaan move_temp_to_location().

            Request body:
            ```json
            { "temp_filename": "20260707_115500_a1b2c3d4_foto.jpg" }
            ```
            """
            try:
                # Pastikan user ada
                user = cls._user_service.get_user_by_id(db, user_id)
                if not user:
                    cls.handle_error(
                        detail=f"User with id {user_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                # Pindahkan file dari temp → uploads/users/avatars/
                file_info = move_temp_to_location(
                    temp_filename=temp_filename,
                    destination="users/avatars",
                )

                # TODO: simpan file_info["file_url"] ke kolom avatar di tabel users
                # cls._user_service.update_avatar(db, user_id, file_info["file_url"])

                return cls.handle_success(
                    data=file_info,
                    message="Avatar updated successfully",
                )
            except FileNotFoundError as e:
                cls.handle_error(
                    detail=str(e), status_code=status.HTTP_404_NOT_FOUND
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


UserController.register_routes()
