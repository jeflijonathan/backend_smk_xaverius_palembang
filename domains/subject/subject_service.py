from typing import List
from sqlalchemy.orm import Session
from domains.subject.subject_repository import SchoolSubjectRepository
from domains.subject.dto.subject_dto import SchoolSubjectCreate, SchoolSubjectUpdate


class SubjectService:
    def __init__(self):
        self.subject_repo = SchoolSubjectRepository()

    def get_subjects(self, db: Session) -> List:
        return self.subject_repo.find_all(db)

    def create_subject(self, db: Session, data: SchoolSubjectCreate):
        return self.subject_repo.create(db, data.dict())

    def update_subject(self, db: Session, id: str, data: SchoolSubjectUpdate):
        return self.subject_repo.update(db, {"id": id}, data.dict(exclude_unset=True))

    def delete_subject(self, db: Session, id: str):
        return self.subject_repo.delete(db, {"id": id})
