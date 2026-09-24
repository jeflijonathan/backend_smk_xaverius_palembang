from typing import List, Optional
from sqlalchemy.orm import Session
from domains.schedule.schedule_repository import (
    CategoryScheduleTimeRepository,
    ScheduleTimeRepository,
    ScheduleRepository,
)
from domains.schedule.dto.schedule_dto import (
    CategoryScheduleTimeCreate,
    CategoryScheduleTimeUpdate,
    ScheduleTimeCreate,
    ScheduleTimeUpdate,
    ScheduleCreate,
    ScheduleUpdate,
)


class ScheduleService:
    def __init__(self):
        self.category_time_repo = CategoryScheduleTimeRepository()
        self.schedule_time_repo = ScheduleTimeRepository()
        self.schedule_repo = ScheduleRepository()

    # CategoryScheduleTime methods
    def get_all_category_times(self, db: Session) -> List:
        return self.category_time_repo.find_all(db)

    def get_category_time_by_id(self, db: Session, id_category: str) -> Optional[object]:
        return self.category_time_repo.find_by_id(db, id_category)

    def create_category_time(self, db: Session, data: CategoryScheduleTimeCreate):
        return self.category_time_repo.create(db, data.dict())

    def update_category_time(self, db: Session, id_category: str, data: CategoryScheduleTimeUpdate):
        return self.category_time_repo.update(
            db, {"id_category_schendule_time": id_category}, data.dict(exclude_unset=True)
        )

    def delete_category_time(self, db: Session, id_category: str):
        return self.category_time_repo.delete(db, {"id_category_schendule_time": id_category})

    # ScheduleTime methods
    def get_all_schedule_times(self, db: Session) -> List:
        return self.schedule_time_repo.find_all(db)

    def get_schedule_time_by_id(self, db: Session, id_time: str) -> Optional[object]:
        return self.schedule_time_repo.find_by_id(db, id_time)

    def create_schedule_time(self, db: Session, data: ScheduleTimeCreate):
        return self.schedule_time_repo.create(db, data.dict())

    def update_schedule_time(self, db: Session, id_time: str, data: ScheduleTimeUpdate):
        return self.schedule_time_repo.update(
            db, {"id_schendule_time": id_time}, data.dict(exclude_unset=True)
        )

    def delete_schedule_time(self, db: Session, id_time: str):
        return self.schedule_time_repo.delete(db, {"id_schendule_time": id_time})

    # Schedule methods
    def get_all_schedules(self, db: Session) -> List:
        return self.schedule_repo.find_all(db)

    def get_schedule_by_id(self, db: Session, id_schendule: str) -> Optional[object]:
        return self.schedule_repo.find_by_id(db, id_schendule)

    def create_schedule(self, db: Session, data: ScheduleCreate):
        return self.schedule_repo.create(db, data.dict())

    def update_schedule(self, db: Session, id_schendule: str, data: ScheduleUpdate):
        return self.schedule_repo.update(
            db, {"id_schendule": id_schendule}, data.dict(exclude_unset=True)
        )

    def delete_schedule(self, db: Session, id_schendule: str):
        return self.schedule_repo.delete(db, {"id_schendule": id_schendule})
