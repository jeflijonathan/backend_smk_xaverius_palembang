from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.classroom.classroom_model import ClassRoomModel


class ClassroomRepository(BaseMySQLService[ClassRoomModel]):
    def __init__(self):
        super().__init__(ClassRoomModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None, paginator: Optional[Dict[str, int]] = None) -> List[ClassRoomModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data, paginator)

    def count_all(self, db: Session, where: Dict[str, Any] = None) -> int:
        filter_data = {"query": where or {}}
        return self.count(db, filter_data)

    def find_by_id(self, db: Session, id_class_room: str) -> Optional[ClassRoomModel]:
        return self.find_one(db, {"id_class_room": id_class_room})

