from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.subject.subject_service import SubjectService
from domains.subject.dto.subject_dto import SchoolSubjectCreate, SchoolSubjectUpdate


class SubjectController(BaseController, prefix="/subjects", tags=["Subjects"]):
    _service = SubjectService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_subjects(db: Session = Depends(get_db)):
            try:
                subjects = cls._service.get_subjects(db)
                return cls.handle_success(
                    data=subjects, message="Subjects retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create_subject(data: SchoolSubjectCreate, db: Session = Depends(get_db)):
            try:
                subject = cls._service.create_subject(db, data)
                return cls.handle_success(
                    data=subject,
                    message="Subject created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id}", status_code=status.HTTP_200_OK)
        def update_subject(id: str, data: SchoolSubjectUpdate, db: Session = Depends(get_db)):
            try:
                subject = cls._service.update_subject(db, id, data)
                if not subject:
                    cls.handle_error(
                        detail=f"Subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=subject, message="Subject updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id}", status_code=status.HTTP_200_OK)
        def delete_subject(id: str, db: Session = Depends(get_db)):
            try:
                subject = cls._service.delete_subject(db, id)
                if not subject:
                    cls.handle_error(
                        detail=f"Subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=subject, message="Subject deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


SubjectController.register_routes()
router = SubjectController.get_router()
