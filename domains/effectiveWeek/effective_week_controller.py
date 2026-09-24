from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.effectiveWeek.effective_week_service import EffectiveWeekService
from domains.effectiveWeek.dto.effective_week_dto import (
    EffectiveWeekCreate,
    EffectiveWeekUpdate,
)


class EffectiveWeekController(
    BaseController, prefix="/effective-weeks", tags=["Effective Weeks"]
):
    _service = EffectiveWeekService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = cls._service.get_all(db)
                return cls.handle_success(
                    data=records, message="Effective weeks retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_effective_week}", status_code=status.HTTP_200_OK)
        def get_by_id(id_effective_week: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.get_by_id(db, id_effective_week)
                if not record:
                    cls.handle_error(
                        detail=f"Effective week with id {id_effective_week} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Effective week retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: EffectiveWeekCreate, db: Session = Depends(get_db)):
            try:
                record = cls._service.create(db, data)
                return cls.handle_success(
                    data=record,
                    message="Effective week created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_effective_week}", status_code=status.HTTP_200_OK)
        def update(
            id_effective_week: str,
            data: EffectiveWeekUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = cls._service.update(db, id_effective_week, data)
                if not record:
                    cls.handle_error(
                        detail=f"Effective week with id {id_effective_week} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Effective week updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_effective_week}", status_code=status.HTTP_200_OK)
        def delete(id_effective_week: str, db: Session = Depends(get_db)):
            try:
                record = cls._service.delete(db, id_effective_week)
                if not record:
                    cls.handle_error(
                        detail=f"Effective week with id {id_effective_week} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Effective week deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


EffectiveWeekController.register_routes()
router = EffectiveWeekController.get_router()
