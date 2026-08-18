from typing import List
from sqlalchemy.orm import Session
from domains.categorySubject.category_subject_repository import CategorySubjectRepository
from domains.categorySubject.dto.category_subject_dto import CategorySubjectCreate, CategorySubjectUpdate


class CategorySubjectService:
    def __init__(self):
        self.repo = CategorySubjectRepository()

    def get_all(self, db: Session) -> List:
        return self.repo.find_all(db)

    def get_by_id(self, db: Session, id: str):
        return self.repo.find_by_id(db, id)

    def create(self, db: Session, data: CategorySubjectCreate):
        existing = db.query(self.repo.model).filter(self.repo.model.name == data.name).first()
        if existing:
            raise ValueError(f"Category subject name '{data.name}' is already registered")
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id: str, data: CategorySubjectUpdate):
        if data.name is not None:
            existing = db.query(self.repo.model).filter(self.repo.model.name == data.name, self.repo.model.id != id).first()
            if existing:
                raise ValueError(f"Category subject name '{data.name}' is already registered")
        return self.repo.update(db, {"id": id}, data.dict(exclude_unset=True))

    def delete(self, db: Session, id: str):
        return self.repo.delete(db, {"id": id})
