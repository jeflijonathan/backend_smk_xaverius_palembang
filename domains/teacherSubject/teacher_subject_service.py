from typing import List, Optional
from sqlalchemy.orm import Session
from domains.teacherSubject.teacher_subject_repository import TeacherSubjectRepository
from domains.teacherSubject.dto.teacher_subject_dto import (
    TeacherSubjectCreate,
    TeacherSubjectUpdate,
)


class TeacherSubjectService:
    def __init__(self):
        self.repo = TeacherSubjectRepository()

    def get_all(self, db: Session) -> List:
        return self.repo.find_all(db)

    def get_by_id(self, db: Session, id_teacher_subject: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_teacher_subject)

    def create(self, db: Session, data: TeacherSubjectCreate):
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id_teacher_subject: str, data: TeacherSubjectUpdate):
        return self.repo.update(
            db, {"id_teacher_subject": id_teacher_subject}, data.dict(exclude_unset=True)
        )

    def delete(self, db: Session, id_teacher_subject: str):
        return self.repo.delete(db, {"id_teacher_subject": id_teacher_subject})
