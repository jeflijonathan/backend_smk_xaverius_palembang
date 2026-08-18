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
        except Exception as error:
            db.rollback()
            raise error

    def find(
        self,
        db: Session,
        filter_data: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, int]] = None,
    ) -> List[ModelType]:
        try:
            filter_data = filter_data or {"query": {}, "sorter": None}
            query_dict = filter_data.get("query", {})
            sorter = filter_data.get("sorter", None)

            stmt = select(self.model)

            if query_dict:
                for key, value in query_dict.items():
                    if hasattr(self.model, key):
                        stmt = stmt.where(getattr(self.model, key) == value)

            if sorter and "sort" in sorter and "order" in sorter:
                if hasattr(self.model, sorter["sort"]):
                    column = getattr(self.model, sorter["sort"])
                    if str(sorter["order"]).lower() == "desc":
                        stmt = stmt.order_by(column.desc())
                    else:
                        stmt = stmt.order_by(column.asc())

            if paginator and "limit" in paginator and "page" in paginator:
                limit = paginator["limit"]
                offset = limit * (paginator["page"] - 1)
                stmt = stmt.limit(limit).offset(offset)

            return list(db.scalars(stmt).all())
        except Exception as error:
            raise error

    def count(self, db: Session, filter_data: Optional[Dict[str, Any]] = None) -> int:
        try:
            filter_data = filter_data or {"query": {}}
            query_dict = filter_data.get("query", {})

            stmt = select(func.count()).select_from(self.model)

            if query_dict:
                for key, value in query_dict.items():
                    if hasattr(self.model, key):
                        stmt = stmt.where(getattr(self.model, key) == value)

            return db.scalar(stmt) or 0
        except Exception as error:
            raise error

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
        except Exception as error:
            raise error

    def update(
        self, db: Session, filter_data: Any, update_data: Dict[str, Any]
    ) -> Optional[ModelType]:
        try:
            where_dict = (
                filter_data if isinstance(filter_data, dict) else {"id": filter_data}
            )

            record = self.find_one(db, where_dict)
            if not record:
                return None

            for key, value in update_data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db.commit()
            db.refresh(record)
            return record
        except Exception as error:
            db.rollback()
            raise error

    def delete(
        self, db: Session, filter_data: Dict[str, Any] = None
    ) -> Optional[ModelType]:
        try:
            filter_data = filter_data or {}
            record = self.find_one(db, filter_data)

            if record:
                db.delete(record)
                db.commit()
                return record

            return None
        except Exception as error:
            db.rollback()
            raise error
