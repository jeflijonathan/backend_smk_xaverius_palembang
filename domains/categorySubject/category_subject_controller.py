from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.categorySubject.category_subject_service import CategorySubjectService
from domains.categorySubject.dto.category_subject_dto import CategorySubjectCreate, CategorySubjectUpdate


class CategorySubjectController(BaseController, prefix="/category-subjects", tags=["Category Subjects"]):
    _service = CategorySubjectService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                categories = cls._service.get_all(db)
                return cls.handle_success(
                    data=categories, message="Category subjects retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id}", status_code=status.HTTP_200_OK)
        def get_by_id(id: str, db: Session = Depends(get_db)):
            try:
                category = cls._service.get_by_id(db, id)
                if not category:
                    cls.handle_error(
                        detail=f"Category subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=category, message="Category subject retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: CategorySubjectCreate, db: Session = Depends(get_db)):
            try:
                category = cls._service.create(db, data)
                return cls.handle_success(
                    data=category,
                    message="Category subject created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error),
                                 status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id}", status_code=status.HTTP_200_OK)
        def update(id: str, data: CategorySubjectUpdate, db: Session = Depends(get_db)):
            try:
                category = cls._service.update(db, id, data)
                if not category:
                    cls.handle_error(
                        detail=f"Category subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=category, message="Category subject updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error),
                                 status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id}", status_code=status.HTTP_200_OK)
        def delete(id: str, db: Session = Depends(get_db)):
            try:
                category = cls._service.delete(db, id)
                if not category:
                    cls.handle_error(
                        detail=f"Category subject with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=category, message="Category subject deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


CategorySubjectController.register_routes()
router = CategorySubjectController.get_router()
