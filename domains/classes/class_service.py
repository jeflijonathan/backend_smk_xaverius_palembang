from typing import List, Optional
from sqlalchemy.orm import Session
from domains.classes.class_repository import ClassRepository
from domains.classes.dto.class_dto import ClassCreate, ClassUpdate


class ClassService:
    def __init__(self):
        self.repo = ClassRepository()

    def get_all(self, db: Session) -> List:
        return self.repo.find_all(db)

    def get_by_id(self, db: Session, id_class: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_class)

    def create(self, db: Session, data: ClassCreate):
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id_class: str, data: ClassUpdate):
        return self.repo.update(db, {"id_class": id_class}, data.dict(exclude_unset=True))

    def delete(self, db: Session, id_class: str):
        return self.repo.delete(db, {"id_class": id_class})
