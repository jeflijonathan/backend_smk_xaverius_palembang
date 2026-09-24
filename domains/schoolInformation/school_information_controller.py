from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.schoolInformation.school_information_service import SchoolInformationService
from domains.schoolInformation.dto.school_information_dto import (
    SchoolInformationCreate,
    SchoolInformationUpdate,
)


class SchoolInformationController(
    BaseController, prefix="/school-informations", tags=["School Information"]
):
    _service = SchoolInformationService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = cls._service.get_all(db)
                return cls.handle_success(
                    data=records, message="School information retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_school_information}", status_code=status.HTTP_200_OK)
        def get_by_id(id_school_information: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.get_by_id(db, id_school_information)
                if not record:
                    cls.handle_error(
                        detail=f"School information with id {id_school_information} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="School information retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: SchoolInformationCreate, db: Session = Depends(get_db)):
            try:
                record = cls._service.create(db, data)
                return cls.handle_success(
                    data=record,
                    message="School information created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_school_information}", status_code=status.HTTP_200_OK)
        def update(
            id_school_information: str,
            data: SchoolInformationUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = cls._service.update(db, id_school_information, data)
                if not record:
                    cls.handle_error(
                        detail=f"School information with id {id_school_information} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="School information updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_school_information}", status_code=status.HTTP_200_OK)
        def delete(id_school_information: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.delete(db, id_school_information)
                if not record:
                    cls.handle_error(
                        detail=f"School information with id {id_school_information} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="School information deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


SchoolInformationController.register_routes()
router = SchoolInformationController.get_router()
