from fastapi import Depends, status, Query
from typing import Optional
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController, PaginationParams
from domains.classes.class_service import ClassService
from domains.classes.dto.class_dto import (
    ClassCreate,
    ClassUpdate,
    ClassResponse,
    StudentSimpleResponse,
    AddStudentsToClassDTO,
)


class ClassController(BaseController, prefix="/classes", tags=["Classes"]):
    _service = ClassService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(
            pagination: PaginationParams = Depends(PaginationParams),
            id_school_information: Optional[str] = Query(default=None),
            id_major: Optional[str] = Query(default=None),
            kelas: Optional[str] = Query(default=None),
            status_param: Optional[str] = Query(default=None, alias="status"),
            db: Session = Depends(get_db),
        ):
            try:
                where = {}
                if id_school_information and id_school_information.strip():
                    where["id_school_information"] = id_school_information.strip()
                if id_major and id_major.strip():
                    where["id_major"] = id_major.strip()
                if kelas and kelas.strip():
                    where["kelas"] = kelas.strip()
                if status_param is not None and status_param.strip() != "":
                    where["status"] = True if status_param.strip().lower() in ("true", "1") else False

                paginator_dict = pagination.to_dict()
                classes = cls._service.get_all(
                    db,
                    where=where,
                    paginator=paginator_dict,
                )
                total_data = cls._service.count_all(
                    db,
                    where=where,
                    search=pagination.value,
                )

                data = [ClassResponse.model_validate(c).model_dump() for c in classes]

                return cls.handle_paginated_success(
                    data=data,
                    total_data=total_data,
                    page=pagination.page,
                    limit=pagination.limit,
                    message="Classes retrieved successfully",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_class}", status_code=status.HTTP_200_OK)
        def get_by_id(id_class: str, db: Session = Depends(get_db)):
            try:
                class_obj = cls._service.get_by_id(db, id_class)
                if not class_obj:
                    cls.handle_error(
                        detail=f"Class with id {id_class} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                res_data = ClassResponse.model_validate(class_obj).model_dump()
                # Attach students & count
                students = cls._service.get_class_students(db, id_class)
                res_data["students"] = [StudentSimpleResponse.model_validate(s).model_dump() for s in students]
                res_data["total_students"] = len(students)
                return cls.handle_success(
                    data=res_data, message="Class retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_class}/students", status_code=status.HTTP_200_OK)
        def get_students(id_class: str, db: Session = Depends(get_db)):
            try:
                students = cls._service.get_class_students(db, id_class)
                data = [StudentSimpleResponse.model_validate(s).model_dump() for s in students]
                return cls.handle_success(
                    data=data, message="Class students retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_class}/available-students", status_code=status.HTTP_200_OK)
        def get_available_students(id_class: str, db: Session = Depends(get_db)):
            try:
                students = cls._service.get_available_students(db, id_class)
                data = [StudentSimpleResponse.model_validate(s).model_dump() for s in students]
                return cls.handle_success(
                    data=data, message="Available students retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/{id_class}/students", status_code=status.HTTP_200_OK)
        def add_students(id_class: str, payload: AddStudentsToClassDTO, db: Session = Depends(get_db)):
            try:
                students = cls._service.add_students_to_class(
                    db, id_class, payload.student_ids, force_transfer=bool(payload.force_transfer)
                )
                data = [StudentSimpleResponse.model_validate(s).model_dump() for s in students]
                action_text = "dipindahkan / ditambahkan" if payload.force_transfer else "ditambahkan"
                return cls.handle_success(
                    data=data,
                    message=f"{len(payload.student_ids)} siswa berhasil {action_text} ke kelas",
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_class}/students/{student_id}", status_code=status.HTTP_200_OK)
        def remove_student(id_class: str, student_id: str, db: Session = Depends(get_db)):
            try:
                success = cls._service.remove_student_from_class(db, id_class, student_id)
                if not success:
                    cls.handle_error(
                        detail="Siswa tidak ditemukan di kelas ini",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data={"id_student": student_id},
                    message="Siswa berhasil dikeluarkan dari kelas",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: ClassCreate, db: Session = Depends(get_db)):
            try:
                class_obj = cls._service.create(db, data)
                res_data = ClassResponse.model_validate(class_obj).model_dump()
                return cls.handle_success(
                    data=res_data,
                    message="Class created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_class}", status_code=status.HTTP_200_OK)
        def update(id_class: str, data: ClassUpdate, db: Session = Depends(get_db)):
            try:
                class_obj = cls._service.update(db, id_class, data)
                if not class_obj:
                    cls.handle_error(
                        detail=f"Class with id {id_class} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                res_data = ClassResponse.model_validate(class_obj).model_dump()
                return cls.handle_success(
                    data=res_data, message="Class updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_class}", status_code=status.HTTP_200_OK)
        def delete(id_class: str, db: Session = Depends(get_db)):
            try:
                class_obj = cls._service.delete(db, id_class)
                if not class_obj:
                    cls.handle_error(
                        detail=f"Class with id {id_class} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=class_obj, message="Class deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


ClassController.register_routes()
router = ClassController.get_router()
