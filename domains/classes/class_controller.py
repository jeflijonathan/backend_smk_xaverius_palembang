from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.classes.class_service import ClassService
from domains.classes.dto.class_dto import ClassCreate, ClassUpdate


class ClassController(BaseController, prefix="/classes", tags=["Classes"]):
    _service = ClassService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                classes = cls._service.get_all(db)
                return cls.handle_success(
                    data=classes, message="Classes retrieved successfully"
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
                return cls.handle_success(
                    data=class_obj, message="Class retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: ClassCreate, db: Session = Depends(get_db)):
            try:
                class_obj = cls._service.create(db, data)
                return cls.handle_success(
                    data=class_obj,
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
                return cls.handle_success(
                    data=class_obj, message="Class updated successfully"
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
