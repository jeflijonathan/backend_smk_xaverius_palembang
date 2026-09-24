from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from domains.categorySubject.category_subject_repository import CategorySubjectRepository
from domains.categorySubject.dto.category_subject_dto import CategorySubjectCreate, CategorySubjectUpdate


class CategorySubjectService:
    def __init__(self):
        self.repo = CategorySubjectRepository()

    def get_all(self, db: Session, paginator: Optional[Dict[str, Any]] = None) -> List:
        return self.repo.find_all(db, paginator=paginator)

    def count_all(self, db: Session) -> int:
        return self.repo.count_all(db)

    def get_by_id(self, db: Session, id: str):
        return self.repo.find_by_id(db, id)

    def create(self, db: Session, data: CategorySubjectCreate):
        existing = self.repo.find_by_name(db, data.name)
        if existing:
            raise ValueError(f"Category subject name '{data.name}' is already registered")

        payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        return self.repo.create(db, payload)

    def update(self, db: Session, id: str, data: CategorySubjectUpdate):
        # 1. Pastikan data yang ingin di-update memang ada
        existing_item = self.repo.find_by_id(db, id)
        if not existing_item:
            return None

        # 2. Cek duplikasi nama jika nama diubah
        if data.name is not None and data.name != existing_item.name:
            duplicate = self.repo.find_by_name(db, data.name)
            if duplicate:
                raise ValueError(f"Category subject name '{data.name}' is already registered")

        # 3. Dump hanya field yang diisi/dikirim oleh client
        update_data = (
            data.model_dump(exclude_unset=True) 
            if hasattr(data, "model_dump") 
            else data.dict(exclude_unset=True)
        )
        
        return self.repo.update(db, {"id": id}, update_data)

    def delete(self, db: Session, id: str):
        existing_item = self.repo.find_by_id(db, id)
        if not existing_item:
            return None
            
        return self.repo.delete(db, {"id": id})