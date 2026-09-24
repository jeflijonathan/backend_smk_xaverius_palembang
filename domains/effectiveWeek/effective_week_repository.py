from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.effectiveWeek.effective_week_model import EffectiveWeekModel


class EffectiveWeekRepository(BaseMySQLService[EffectiveWeekModel]):
    def __init__(self):
        super().__init__(EffectiveWeekModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[EffectiveWeekModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_effective_week: str) -> Optional[EffectiveWeekModel]:
        return self.find_one(db, {"id_effective_week": id_effective_week})
