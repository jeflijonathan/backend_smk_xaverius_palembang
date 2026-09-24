from typing import List, Optional
from sqlalchemy.orm import Session
from domains.classroom.classroom_repository import ClassroomRepository
from domains.classroom.dto.classroom_dto import ClassroomCreate, ClassroomUpdate


class ClassroomService:
    def __init__(self):
        self.repo = ClassroomRepository()

    def get_all(self, db: Session) -> List:
        return self.repo.find_all(db)

    def get_by_id(self, db: Session, id_class_room: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_class_room)

    def create(self, db: Session, data: ClassroomCreate):
        return self.repo.create(db, data.dict())

    def update(self, db: Session, id_class_room: str, data: ClassroomUpdate):
        return self.repo.update(
            db, {"id_class_room": id_class_room}, data.dict(exclude_unset=True)
        )

    def delete(self, db: Session, id_class_room: str):
        return self.repo.delete(db, {"id_class_room": id_class_room})
