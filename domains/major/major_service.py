from typing import List, Optional
from sqlalchemy.orm import Session
from domains.major.major_repository import MajorRepository
from domains.major.dto.major_dto import MajorCreate, MajorUpdate


class MajorService:
    def __init__(self):
        self.major_repo = MajorRepository()

    def get_majors(self, db: Session) -> List:
        return self.major_repo.find_all(db)

    def get_major_by_id(self, db: Session, id_major: str) -> Optional[object]:
        return self.major_repo.find_by_id(db, id_major)

    def create_major(self, db: Session, data: MajorCreate):
        return self.major_repo.create(db, data.dict())

    def update_major(self, db: Session, id_major: str, data: MajorUpdate):
        return self.major_repo.update(db, {"id_major": id_major}, data.dict(exclude_unset=True))

    def delete_major(self, db: Session, id_major: str):
        return self.major_repo.delete(db, {"id_major": id_major})
