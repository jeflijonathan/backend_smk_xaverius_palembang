from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.major.major_service import MajorService
from domains.major.dto.major_dto import MajorCreate, MajorUpdate


class MajorController(BaseController, prefix="/majors", tags=["Majors"]):
    _service = MajorService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_majors(db: Session = Depends(get_db)):
            try:
                majors = cls._service.get_majors(db)
                return cls.handle_success(
                    data=majors, message="Majors retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_major}", status_code=status.HTTP_200_OK)
        def get_major(id_major: str, db: Session = Depends(get_db)):
            try:
                major = cls._service.get_major_by_id(db, id_major)
                if not major:
                    cls.handle_error(
                        detail=f"Major with id {id_major} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=major, message="Major retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create_major(data: MajorCreate, db: Session = Depends(get_db)):
            try:
                major = cls._service.create_major(db, data)
                return cls.handle_success(
                    data=major,
                    message="Major created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_major}", status_code=status.HTTP_200_OK)
        def update_major(id_major: str, data: MajorUpdate, db: Session = Depends(get_db)):
            try:
                major = cls._service.update_major(db, id_major, data)
                if not major:
                    cls.handle_error(
                        detail=f"Major with id {id_major} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=major, message="Major updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_major}", status_code=status.HTTP_200_OK)
        def delete_major(id_major: str, db: Session = Depends(get_db)):
            try:
                major = cls._service.delete_major(db, id_major)
                if not major:
                    cls.handle_error(
                        detail=f"Major with id {id_major} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=major, message="Major deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


MajorController.register_routes()
router = MajorController.get_router()
