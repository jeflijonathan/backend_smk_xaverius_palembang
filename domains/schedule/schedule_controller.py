from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.schedule.schedule_service import ScheduleService
from domains.schedule.dto.schedule_dto import (
    CategoryScheduleTimeCreate,
    CategoryScheduleTimeUpdate,
    ScheduleTimeCreate,
    ScheduleTimeUpdate,
    ScheduleCreate,
    ScheduleUpdate,
)

_service = ScheduleService()


class CategoryScheduleTimeController(
    BaseController, prefix="/category-schedule-times", tags=["Category Schedule Times"]
):
    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = _service.get_all_category_times(db)
                return cls.handle_success(
                    data=records, message="Category schedule times retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_category}", status_code=status.HTTP_200_OK)
        def get_by_id(id_category: str, db: Session = Depends(get_db)):
            try:
                record = _service.get_category_time_by_id(db, id_category)
                if not record:
                    cls.handle_error(
                        detail=f"Category schedule time with id {id_category} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Category schedule time retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: CategoryScheduleTimeCreate, db: Session = Depends(get_db)):
            try:
                record = _service.create_category_time(db, data)
                return cls.handle_success(
                    data=record,
                    message="Category schedule time created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_category}", status_code=status.HTTP_200_OK)
        def update(
            id_category: str,
            data: CategoryScheduleTimeUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = _service.update_category_time(db, id_category, data)
                if not record:
                    cls.handle_error(
                        detail=f"Category schedule time with id {id_category} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Category schedule time updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_category}", status_code=status.HTTP_200_OK)
        def delete(id_category: str, db: Session = Depends(get_db)):
            try:
                record = _service.delete_category_time(db, id_category)
                if not record:
                    cls.handle_error(
                        detail=f"Category schedule time with id {id_category} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Category schedule time deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


class ScheduleTimeController(
    BaseController, prefix="/schedule-times", tags=["Schedule Times"]
):
    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = _service.get_all_schedule_times(db)
                return cls.handle_success(
                    data=records, message="Schedule times retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_time}", status_code=status.HTTP_200_OK)
        def get_by_id(id_time: str, db: Session = Depends(get_db)):
            try:
                record = _service.get_schedule_time_by_id(db, id_time)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule time with id {id_time} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule time retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: ScheduleTimeCreate, db: Session = Depends(get_db)):
            try:
                record = _service.create_schedule_time(db, data)
                return cls.handle_success(
                    data=record,
                    message="Schedule time created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_time}", status_code=status.HTTP_200_OK)
        def update(
            id_time: str,
            data: ScheduleTimeUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = _service.update_schedule_time(db, id_time, data)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule time with id {id_time} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule time updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_time}", status_code=status.HTTP_200_OK)
        def delete(id_time: str, db: Session = Depends(get_db)):
            try:
                record = _service.delete_schedule_time(db, id_time)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule time with id {id_time} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule time deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


class ScheduleController(
    BaseController, prefix="/schedules", tags=["Schedules"]
):
    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                records = _service.get_all_schedules(db)
                return cls.handle_success(
                    data=records, message="Schedules retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.get("/{id_schendule}", status_code=status.HTTP_200_OK)
        def get_by_id(id_schendule: str, db: Session = Depends(get_db)):
            try:
                record = _service.get_schedule_by_id(db, id_schendule)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule with id {id_schendule} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(data: ScheduleCreate, db: Session = Depends(get_db)):
            try:
                record = _service.create_schedule(db, data)
                return cls.handle_success(
                    data=record,
                    message="Schedule created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id_schendule}", status_code=status.HTTP_200_OK)
        def update(
            id_schendule: str,
            data: ScheduleUpdate,
            db: Session = Depends(get_db),
        ):
            try:
                record = _service.update_schedule(db, id_schendule, data)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule with id {id_schendule} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id_schendule}", status_code=status.HTTP_200_OK)
        def delete(id_schendule: str, db: Session = Depends(get_db)):
            try:
                record = _service.delete_schedule(db, id_schendule)
                if not record:
                    cls.handle_error(
                        detail=f"Schedule with id {id_schendule} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=record, message="Schedule deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


CategoryScheduleTimeController.register_routes()
ScheduleTimeController.register_routes()
ScheduleController.register_routes()
