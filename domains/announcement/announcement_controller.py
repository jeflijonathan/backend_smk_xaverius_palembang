from fastapi import Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.database.db import get_db
from common.base.baseController import BaseController, PaginationParams
from domains.announcement.announcement_service import AnnouncementService
from domains.announcement.dto.announcement_dto import (
    AnnouncementCreateDTO,
    AnnouncementUpdateDTO,
)


def _friendly_db_error(error: IntegrityError) -> str:
    """Convert raw DB errors to user-friendly messages."""
    msg = str(error.orig) if error.orig else str(error)
    if "foreign key constraint fails" in msg.lower() or "1452" in msg:
        if "id_user" in msg:
            return "User yang dipilih tidak ditemukan di database."
        return "Data referensi tidak ditemukan di database."
    if "duplicate entry" in msg.lower() or "1062" in msg:
        return "Data sudah ada, tidak boleh duplikat."
    return "Terjadi kesalahan pada database. Silakan coba lagi."


class AnnouncementController(
    BaseController, prefix="/announcement", tags=["Announcement"]
):
    _service = AnnouncementService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(pagination: PaginationParams = Depends(PaginationParams), db: Session = Depends(get_db)):
            try:
                paginator_dict = pagination.to_dict()
                records = cls._service.get_all(db, paginator=paginator_dict)
                total_data = cls._service.count_all(db)
                return cls.handle_paginated_success(
                    data=records,
                    total_data=total_data,
                    page=pagination.page,
                    limit=pagination.limit,
                    message="Announcement retrieved successfully",
                )
            except Exception as error:
                print(f"DEBUG ERROR ANNOUNCEMENT: {str(error)}")
                import traceback
                traceback.print_exc()
                cls.handle_error(detail=f"Error asli: {str(error)}")

        @cls.router.get("/{id_announcement}", status_code=status.HTTP_200_OK)
        def get_by_id(id_announcement: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.get_by_id(db, id_announcement)
                if not record:
                    cls.handle_error(
                        detail=f"Pengumuman dengan id {id_announcement} tidak ditemukan.",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Announcement retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail="Gagal mengambil detail pengumuman.")

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: AnnouncementCreateDTO, db: Session = Depends(get_db)):
            try:
                record = cls._service.create(db, data)
                return cls.handle_success(
                    data=record,
                    message="Pengumuman berhasil dibuat.",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as error:
                db.rollback()
                cls.handle_error(
                    detail=_friendly_db_error(error),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as error:
                cls.handle_error(detail="Gagal membuat pengumuman. Silakan coba lagi.")

        @cls.router.patch("/{id_announcement}", status_code=status.HTTP_200_OK)
        def update(
            id_announcement: str,
            data: AnnouncementUpdateDTO,
            db: Session = Depends(get_db),
        ):
            try:
                record = cls._service.update(db, id_announcement, data)
                if not record:
                    cls.handle_error(
                        detail=f"Pengumuman dengan id {id_announcement} tidak ditemukan.",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Pengumuman berhasil diperbarui."
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as error:
                db.rollback()
                cls.handle_error(
                    detail=_friendly_db_error(error),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as error:
                cls.handle_error(detail="Gagal memperbarui pengumuman. Silakan coba lagi.")

        @cls.router.delete("/{id_announcement}", status_code=status.HTTP_200_OK)
        def delete(id_announcement: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.delete(db, id_announcement)
                if not record:
                    cls.handle_error(
                        detail=f"Pengumuman dengan id {id_announcement} tidak ditemukan.",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Pengumuman berhasil dihapus."
                )
            except Exception as error:
                cls.handle_error(detail="Gagal menghapus pengumuman. Silakan coba lagi.")


AnnouncementController.register_routes()
router = AnnouncementController.get_router()

