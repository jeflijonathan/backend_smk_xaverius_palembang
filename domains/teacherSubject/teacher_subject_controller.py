from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.teacherSubject.teacher_subject_service import TeacherSubjectService
from domains.teacherSubject.dto.teacher_subject_dto import (
    TeacherSubjectCreate,
    TeacherSubjectUpdate,
)


class TeacherSubjectController(
    BaseController, prefix="/teacher-subjects", tags=["Teacher Subjects"]
):
    _service = TeacherSubjectService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = cls._service.get_all(db)
                return cls.handle_success(
                    data=records, message="Teacher subjects retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_teacher_subject}", status_code=status.HTTP_200_OK)
        def get_by_id(id_teacher_subject: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.get_by_id(db, id_teacher_subject)
                if not record:
                    cls.handle_error(
                        detail=f"Teacher subject with id {id_teacher_subject} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Teacher subject retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: TeacherSubjectCreate, db: Session = Depends(get_db)):
            try:
                record = cls._service.create(db, data)
                return cls.handle_success(
                    data=record,
                    message="Teacher subject created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_teacher_subject}", status_code=status.HTTP_200_OK)
        def update(
            id_teacher_subject: str,
            data: TeacherSubjectUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = cls._service.update(db, id_teacher_subject, data)
                if not record:
                    cls.handle_error(
                        detail=f"Teacher subject with id {id_teacher_subject} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Teacher subject updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_teacher_subject}", status_code=status.HTTP_200_OK)
        def delete(id_teacher_subject: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.delete(db, id_teacher_subject)
                if not record:
                    cls.handle_error(
                        detail=f"Teacher subject with id {id_teacher_subject} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Teacher subject deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


TeacherSubjectController.register_routes()
router = TeacherSubjectController.get_router()
