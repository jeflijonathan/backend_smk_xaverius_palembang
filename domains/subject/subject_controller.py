from fastapi import Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from config.database.db import get_db
from common.base.baseController import BaseController, PaginationParams
from domains.subject.subject_service import SubjectService
from domains.subject.dto.subject_dto import (
    SchoolSubjectCreate,
    SchoolSubjectUpdate,
    SchoolSubjectResponse,
)


class SubjectController(BaseController, prefix="/subjects", tags=["Subjects"]):
    _service = SubjectService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_subjects(
            pagination: PaginationParams = Depends(),
            id_category_subject: Optional[str] = Query(default=None),
            id_major: Optional[str] = Query(default=None),
            kelas: Optional[str] = Query(default=None),
            fase: Optional[str] = Query(default=None),
            status_param: Optional[bool] = Query(default=None, alias="status"),
            db: Session = Depends(get_db),
        ):
            try:
                paginator_dict = pagination.to_dict()
                where = {}
                if id_category_subject:
                    where["id_category_subject"] = id_category_subject
                if id_major:
                    where["id_major"] = id_major
                if kelas:
                    where["kelas"] = kelas
                if fase:
                    where["fase"] = fase
                if status_param is not None:
                    where["status"] = status_param

                subjects = cls._service.get_all(db, paginator=paginator_dict, where=where)
                total_data = cls._service.count_all(
                    db,
                    where=where,
                    search=pagination.value,
                )

                data = [SchoolSubjectResponse.model_validate(subj).model_dump() for subj in subjects]

                return cls.handle_paginated_success(
                    data=data,
                    total_data=total_data,
                    page=pagination.page,
                    limit=pagination.limit,
                    message="Subjects retrieved successfully",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id}", status_code=status.HTTP_200_OK)
        def get_subject(id: str, db: Session = Depends(get_db)):
            try:
                subject = cls._service.get_by_id(db, id)
                if not subject:
                    cls.handle_error(
                        detail=f"Subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                res_data = SchoolSubjectResponse.model_validate(subject).model_dump()
                return cls.handle_success(
                    data=res_data, message="Subject retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create_subject(data: SchoolSubjectCreate, db: Session = Depends(get_db)):
            try:
                subject = cls._service.create_subject(db, data)
                res_data = SchoolSubjectResponse.model_validate(subject).model_dump()
                return cls.handle_success(
                    data=res_data,
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
                res_data = SchoolSubjectResponse.model_validate(subject).model_dump()
                return cls.handle_success(
                    data=res_data, message="Subject updated successfully"
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
                    data={"id": id}, message="Subject deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


SubjectController.register_routes()
router = SubjectController.get_router()
