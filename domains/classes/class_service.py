from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from domains.classes.class_repository import ClassRepository
from domains.classes.class_model import ClassModel
from domains.classes.dto.class_dto import ClassCreate, ClassUpdate


class ClassService:
    def __init__(self):
        self.repo = ClassRepository()

    def get_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, Any]] = None,
    ) -> List:
        search = paginator.get("value") if paginator else None
        sort = paginator.get("sort") if paginator else None
        order_by = paginator.get("order_by") if paginator else None
        return self.repo.find_all(
            db,
            where=where,
            paginator=paginator,
            search=search,
            sort=sort,
            order_by=order_by,
        )

    def count_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
    ) -> int:
        return self.repo.count_all(db, where=where, search=search)

    def get_by_id(self, db: Session, id_class: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_class)

    def _validate_unique_guardian(
        self,
        db: Session,
        guardian_id: Optional[str],
        school_info_id: Optional[str],
        exclude_class_id: Optional[str] = None,
    ):
        if not guardian_id:
            return

        stmt = select(ClassModel).where(ClassModel.id_class_guardian == guardian_id)
        if school_info_id:
            stmt = stmt.where(ClassModel.id_school_information == school_info_id)
        if exclude_class_id:
            stmt = stmt.where(ClassModel.id_class != exclude_class_id)

        existing = db.scalars(stmt).first()
        if existing:
            class_name = existing.name or existing.kelas or "lain"
            raise ValueError(
                f"Guru ini sudah menjadi wali kelas untuk kelas '{class_name}'. Setiap guru hanya dapat menjadi wali kelas untuk 1 kelas."
            )

    def create(self, db: Session, data: ClassCreate):
        payload = data.dict()
        if not payload.get("name") and payload.get("kelas"):
            payload["name"] = payload.get("kelas")
        elif not payload.get("kelas") and payload.get("name"):
            payload["kelas"] = payload.get("name")

        self._validate_unique_guardian(
            db,
            guardian_id=payload.get("id_class_guardian"),
            school_info_id=payload.get("id_school_information"),
        )

        return self.repo.create(db, payload)

    def update(self, db: Session, id_class: str, data: ClassUpdate):
        payload = data.dict(exclude_unset=True)
        if "kelas" in payload and not payload.get("name"):
            payload["name"] = payload.get("kelas")

        if "id_class_guardian" in payload:
            existing_class = self.get_by_id(db, id_class)
            school_info_id = payload.get("id_school_information") or (
                existing_class.id_school_information if existing_class else None
            )
            self._validate_unique_guardian(
                db,
                guardian_id=payload.get("id_class_guardian"),
                school_info_id=school_info_id,
                exclude_class_id=id_class,
            )

        return self.repo.update(db, {"id_class": id_class}, payload)

    def delete(self, db: Session, id_class: str):
        return self.repo.delete(db, {"id_class": id_class})

    def get_class_students(self, db: Session, id_class: str):
        return self.repo.get_class_students(db, id_class)

    def add_students_to_class(
        self, db: Session, id_class: str, student_ids: List[str], force_transfer: bool = False
    ):
        return self.repo.add_students_to_class(
            db, id_class, student_ids, force_transfer=force_transfer
        )

    def remove_student_from_class(self, db: Session, id_class: str, student_id: str):
        return self.repo.remove_student_from_class(db, id_class, student_id)

    def get_available_students(self, db: Session, id_class: str):
        return self.repo.get_available_students(db, id_class)

