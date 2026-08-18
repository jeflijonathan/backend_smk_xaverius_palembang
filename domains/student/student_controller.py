from fastapi import Depends, status, Body
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from common.utils.file_location import move_temp_to_location
from domains.student.student_service import StudentService
from domains.student.dto.student_dto import CreateStudentDTO, UpdateStudentDTO


class StudentController(BaseController, prefix="/students", tags=["Students"]):
    _student_service = StudentService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                students = cls._student_service.get_all_students(db)
                return cls.handle_success(
                    data=students, message="Students retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))
                
        @cls.router.get("/{student_id}", status_code=status.HTTP_200_OK)
        def get_by_id(student_id: str, db: Session = Depends(get_db)):
            try:
                student = cls._student_service.get_student_by_id(db, student_id)
                if not student:
                    cls.handle_error(
                        detail=f"Student with id {student_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=student, message="Student retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(student_data: CreateStudentDTO, db: Session = Depends(get_db)):
            try:
                student = cls._student_service.create_student(db, student_data)
                return cls.handle_success(
                    data=student,
                    message="Student created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.put("/{student_id}", status_code=status.HTTP_200_OK)
        def update_student(
            student_id: str, update_data: UpdateStudentDTO, db: Session = Depends(get_db)
        ):
            try:
                student = cls._student_service.update_student(db, student_id, update_data)
                if not student:
                    cls.handle_error(
                        detail=f"Student with id {student_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=student, message="Student updated successfully"
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))
                
        @cls.router.delete("/{student_id}", status_code=status.HTTP_200_OK)
        def delete_student(student_id: str, db: Session = Depends(get_db)):
            try:
                student = cls._student_service.delete_student(db, student_id)
                return cls.handle_success(
                    data=student, message="Student deleted successfully"
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.put("/{student_id}/avatar", status_code=status.HTTP_200_OK)
        def update_avatar(
            student_id: str,
            temp_filename: str = Body(..., embed=True,
                                      description="temp_filename dari response POST /api/upload/"),
            db: Session = Depends(get_db),
        ):
            """
            Contoh penggunaan move_temp_to_location().
            """
            try:
                student = cls._student_service.get_student_by_id(db, student_id)
                if not student:
                    cls.handle_error(
                        detail=f"Student with id {student_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                file_info = move_temp_to_location(
                    temp_filename=temp_filename,
                    destination="students/avatars",
                )

                # TODO: simpan file_info["file_url"] ke tabel students/upload_file
                # cls._student_service.update_avatar(db, student_id, file_info["file_url"])

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


StudentController.register_routes()
