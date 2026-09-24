from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.categorySubject.category_subject_model import CategorySubjectModel


class CategorySubjectRepository(BaseMySQLService[CategorySubjectModel]):
    def __init__(self):
        super().__init__(CategorySubjectModel)

    def find_all(
        self, 
        db: Session, 
        where: Optional[Dict[str, Any]] = None, 
        paginator: Optional[Dict[str, int]] = None
    ) -> List[CategorySubjectModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data, paginator)

    def count_all(self, db: Session, where: Optional[Dict[str, Any]] = None) -> int:
        filter_data = {"query": where or {}}
        return self.count(db, filter_data)

    def find_by_id(self, db: Session, id: str) -> Optional[CategorySubjectModel]:
        return self.find_one(db, {"id_category_subject": id})

    def find_by_name(self, db: Session, name: str) -> Optional[CategorySubjectModel]:
        return self.find_one(db, {"name": name})