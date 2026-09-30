from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from config.database.db import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseMySQLService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, data: Dict[str, Any]) -> ModelType:
        try:
            db_obj = self.model(**data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception:
            db.rollback()
            raise

    def find(
        self,
        db: Session,
        filter_data: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, Any]] = None,
        options: Optional[List[Any]] = None,
    ) -> List[ModelType]:
        try:
            filter_data = filter_data or {}
            query_dict = filter_data.get("query", {})
            sorter = filter_data.get("sorter", None)

            stmt = select(self.model)

            if options:
                for opt in options:
                    stmt = stmt.options(opt)

            if query_dict:
                for key, value in query_dict.items():
                    if hasattr(self.model, key) and value is not None:
                        stmt = stmt.where(getattr(self.model, key) == value)

            if sorter and "sort" in sorter and "order" in sorter:
                if hasattr(self.model, sorter["sort"]):
                    column = getattr(self.model, sorter["sort"])
                    if str(sorter["order"]).lower() == "desc":
                        stmt = stmt.order_by(column.desc())
                    else:
                        stmt = stmt.order_by(column.asc())

            if paginator:
                page = int(paginator.get("page", 1))
                limit = paginator.get("limit")

                if limit is not None and int(limit) > 0:
                    limit = int(limit)
                    offset = (page - 1) * limit
                    # Urutan yang benar: offset dulu baru limit
                    stmt = stmt.offset(offset).limit(limit)

            return list(db.scalars(stmt).all())
        except Exception:
            raise

    def count(self, db: Session, filter_data: Optional[Dict[str, Any]] = None) -> int:
        try:
            filter_data = filter_data or {}
            query_dict = filter_data.get("query", {})

            stmt = select(func.count()).select_from(self.model)

            if query_dict:
                for key, value in query_dict.items():
                    if hasattr(self.model, key) and value is not None:
                        stmt = stmt.where(getattr(self.model, key) == value)

            return db.scalar(stmt) or 0
        except Exception:
            raise

    def find_one(
        self, db: Session, filter_data: Optional[Dict[str, Any]] = None
    ) -> Optional[ModelType]:
        try:
            filter_data = filter_data or {}
            stmt = select(self.model)

            for key, value in filter_data.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)

            return db.scalars(stmt).first()
        except Exception:
            raise

    def update(
        self, db: Session, filter_data: Dict[str, Any], update_data: Dict[str, Any]
    ) -> Optional[ModelType]:
        try:
            if not isinstance(filter_data, dict):
                raise ValueError("filter_data harus berupa dictionary, contoh: {'id_category_subject': id}")

            record = self.find_one(db, filter_data)
            if not record:
                return None

            for key, value in update_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.commit()
            db.refresh(record)
            return record
        except Exception:
            db.rollback()
            raise

    def delete(
        self, db: Session, filter_data: Optional[Dict[str, Any]] = None
    ) -> Optional[ModelType]:
        try:
            filter_data = filter_data or {}
            record = self.find_one(db, filter_data)

            if record:
                db.delete(record)
                db.commit()
                return record

            return None
        except Exception:
            db.rollback()
            raise