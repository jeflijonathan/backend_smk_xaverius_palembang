from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.classroom.classroom_service import ClassroomService
from domains.classroom.dto.classroom_dto import ClassroomCreate, ClassroomUpdate


class ClassroomController(BaseController, prefix="/classrooms", tags=["Classrooms"]):
    _service = ClassroomService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = cls._service.get_all(db)
                return cls.handle_success(
                    data=records, message="Classrooms retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_class_room}", status_code=status.HTTP_200_OK)
        def get_by_id(id_class_room: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.get_by_id(db, id_class_room)
                if not record:
                    cls.handle_error(
                        detail=f"Classroom with id {id_class_room} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Classroom retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: ClassroomCreate, db: Session = Depends(get_db)):
            try:
                record = cls._service.create(db, data)
                return cls.handle_success(
                    data=record,
                    message="Classroom created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_class_room}", status_code=status.HTTP_200_OK)
        def update(
            id_class_room: str, data: ClassroomUpdate, db: Session = Depends(get_db)
        ):
            try:
                record = cls._service.update(db, id_class_room, data)
                if not record:
                    cls.handle_error(
                        detail=f"Classroom with id {id_class_room} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Classroom updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_class_room}", status_code=status.HTTP_200_OK)
        def delete(id_class_room: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.delete(db, id_class_room)
                if not record:
                    cls.handle_error(
                        detail=f"Classroom with id {id_class_room} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Classroom deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


ClassroomController.register_routes()
router = ClassroomController.get_router()
