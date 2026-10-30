from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from domains.subject.subject_repository import SchoolSubjectRepository
from domains.subject.dto.subject_dto import SchoolSubjectCreate, SchoolSubjectUpdate


def calculate_fase(kelas: Optional[str]) -> Optional[str]:
    if not kelas:
        return None
    k = str(kelas).strip()
    if k == "10":
        return "E"
    elif k in ("11", "12"):
        return "F"
    return None


class SubjectService:
    def __init__(self):
        self.repo = SchoolSubjectRepository()

    def get_all(
        self,
        db: Session,
        paginator: Optional[Dict[str, Any]] = None,
        where: Optional[Dict[str, Any]] = None,
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

    def get_by_id(self, db: Session, id_subject: str) -> Optional[object]:
        return self.repo.find_by_id(db, id_subject)

    def create_subject(self, db: Session, data: SchoolSubjectCreate):
        create_data = data.dict(exclude_unset=True)
        cat_id = data.get_category_subject_id()
        if cat_id:
            create_data["id_category_subject"] = cat_id
            create_data.pop("category_subject_id", None)

        # Auto-compute fase if kelas is provided
        if create_data.get("kelas"):
            create_data["fase"] = calculate_fase(create_data["kelas"])

        created = self.repo.create(db, create_data)
        return self.get_by_id(db, created.id_subject)

    def update_subject(self, db: Session, id: str, data: SchoolSubjectUpdate):
        update_data = data.dict(exclude_unset=True)
        if "category_subject_id" in update_data and not update_data.get("id_category_subject"):
            update_data["id_category_subject"] = update_data.pop("category_subject_id")

        # Auto-compute fase if kelas is provided
        if "kelas" in update_data:
            update_data["fase"] = calculate_fase(update_data.get("kelas"))

        updated = self.repo.update(db, {"id_subject": id}, update_data)
        if not updated:
            return None
        return self.get_by_id(db, id)

    def delete_subject(self, db: Session, id: str):
        return self.repo.delete(db, {"id_subject": id})
