from typing import List, Optional
from sqlalchemy.orm import Session
from domains.subject.subject_repository import SchoolSubjectRepository
from domains.subject.dto.subject_dto import SchoolSubjectCreate, SchoolSubjectUpdate


class SubjectService:
    def __init__(self):
        self.subject_repo = SchoolSubjectRepository()

    def get_subjects(self, db: Session) -> List:
        return self.subject_repo.find_all(db)

    def get_subject_by_id(self, db: Session, id_subject: str) -> Optional[object]:
        return self.subject_repo.find_by_id(db, id_subject)

    def create_subject(self, db: Session, data: SchoolSubjectCreate):
        create_data = data.dict(exclude_unset=True)
        cat_id = data.get_category_subject_id()
        if cat_id:
            create_data["id_category_subject"] = cat_id
            create_data.pop("category_subject_id", None)
        return self.subject_repo.create(db, create_data)

    def update_subject(self, db: Session, id: str, data: SchoolSubjectUpdate):
        update_data = data.dict(exclude_unset=True)
        if "category_subject_id" in update_data and not update_data.get("id_category_subject"):
            update_data["id_category_subject"] = update_data.pop("category_subject_id")
        return self.subject_repo.update(db, {"id_subject": id}, update_data)

    def delete_subject(self, db: Session, id: str):
        return self.subject_repo.delete(db, {"id_subject": id})
