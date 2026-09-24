from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.schedule.schedule_model import (
    CategoryScheduleTimeModel,
    ScheduleTimeModel,
    ScheduleModel,
)


class CategoryScheduleTimeRepository(BaseMySQLService[CategoryScheduleTimeModel]):
    def __init__(self):
        super().__init__(CategoryScheduleTimeModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[CategoryScheduleTimeModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_category_schendule_time: str) -> Optional[CategoryScheduleTimeModel]:
        return self.find_one(db, {"id_category_schendule_time": id_category_schendule_time})


class ScheduleTimeRepository(BaseMySQLService[ScheduleTimeModel]):
    def __init__(self):
        super().__init__(ScheduleTimeModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[ScheduleTimeModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_schendule_time: str) -> Optional[ScheduleTimeModel]:
        return self.find_one(db, {"id_schendule_time": id_schendule_time})


class ScheduleRepository(BaseMySQLService[ScheduleModel]):
    def __init__(self):
        super().__init__(ScheduleModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[ScheduleModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_schendule: str) -> Optional[ScheduleModel]:
        return self.find_one(db, {"id_schendule": id_schendule})
