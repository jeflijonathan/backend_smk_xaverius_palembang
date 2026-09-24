from typing import List, Optional
from sqlalchemy.orm import Session
from domains.effectiveWeek.effective_week_repository import EffectiveWeekRepository
from domains.effectiveWeek.dto.effective_week_dto import (
    EffectiveWeekCreate,
    EffectiveWeekUpdate,
)


class EffectiveWeekService:
    def __init__(self):
        self.repo = EffectiveWeekRepository()

    def get_all(self, db: Session) -> List:
        return self.repo.find_all(db)

    def get_by_id(self, db: Session, id_effective_week: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_effective_week)

    def create(self, db: Session, data: EffectiveWeekCreate):
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id_effective_week: str, data: EffectiveWeekUpdate):
        return self.repo.update(
            db, {"id_effective_week": id_effective_week}, data.dict(exclude_unset=True)
        )

    def delete(self, db: Session, id_effective_week: str):
        return self.repo.delete(db, {"id_effective_week": id_effective_week})
