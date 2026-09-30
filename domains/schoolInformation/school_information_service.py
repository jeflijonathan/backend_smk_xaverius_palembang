from typing import List, Optional
from sqlalchemy.orm import Session
from domains.schoolInformation.school_information_repository import SchoolInformationRepository
from domains.schoolInformation.dto.school_information_dto import (
    SchoolInformationCreate,
    SchoolInformationUpdate,
)


class SchoolInformationService:
    def __init__(self):
        self.repo = SchoolInformationRepository()

    def get_all(self, db: Session, paginator: dict) -> List:
        return self.repo.find_all(db, paginator=paginator)

    def count_all(self, db: Session) -> int:
        return self.repo.count_all(db)

    def get_by_id(self, db: Session, id_school_information: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_school_information)

    def create(self, db: Session, data: SchoolInformationCreate):
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id_school_information: str, data: SchoolInformationUpdate):
        return self.repo.update(
            db, {"id_school_information": id_school_information}, data.dict(exclude_unset=True)
        )

    def delete(self, db: Session, id_school_information: str):
        return self.repo.delete(db, {"id_school_information": id_school_information})
