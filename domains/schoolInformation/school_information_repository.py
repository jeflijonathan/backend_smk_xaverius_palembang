from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.schoolInformation.school_information_model import SchoolInformationModel


class SchoolInformationRepository(BaseMySQLService[SchoolInformationModel]):
    def __init__(self):
        super().__init__(SchoolInformationModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[SchoolInformationModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_school_information: str) -> Optional[SchoolInformationModel]:
        return self.find_one(db, {"id_school_information": id_school_information})
