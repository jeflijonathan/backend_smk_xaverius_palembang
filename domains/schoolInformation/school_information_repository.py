from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.schoolInformation.school_information_model import SchoolInformationModel


class SchoolInformationRepository(BaseMySQLService[SchoolInformationModel]):
    def __init__(self):
        super().__init__(SchoolInformationModel)

    def find_all(
        self, 
        db: Session, 
        where: Optional[Dict[str, Any]] = None, 
        paginator: Optional[Dict[str, int]] = None
    ) -> List[SchoolInformationModel]:
        filter_data = {"query": where or {}}
        options = [joinedload(SchoolInformationModel.headmaster)]
        return self.find(db, filter_data, paginator, options)

    def count_all(self, db: Session) -> int:
        return self.count(db)

    def find_by_id(self, db: Session, id_school_information: str) -> Optional[SchoolInformationModel]:
        options = [joinedload(SchoolInformationModel.headmaster)]
        return self.find_one(db, {"id_school_information": id_school_information}, options)
    