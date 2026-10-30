from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, asc, desc, func
from common.base.baseMysql import BaseMySQLService
from domains.subject.subject_model import SchoolSubjectModel


class SchoolSubjectRepository(BaseMySQLService[SchoolSubjectModel]):
    def __init__(self):
        super().__init__(SchoolSubjectModel)

    def find_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> List[SchoolSubjectModel]:
        stmt = (
            select(SchoolSubjectModel)
            .options(
                joinedload(SchoolSubjectModel.category),
                joinedload(SchoolSubjectModel.major),
            )
            .where(SchoolSubjectModel.deleted_at.is_(None))
        )

        if where:
            for k, v in where.items():
                if hasattr(SchoolSubjectModel, k) and v is not None and v != "":
                    stmt = stmt.where(getattr(SchoolSubjectModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    SchoolSubjectModel.name.ilike(kw),
                    SchoolSubjectModel.code_subject.ilike(kw),
                    SchoolSubjectModel.id_subject.ilike(kw),
                )
            )

        valid_sort_cols = {
            "name",
            "code_subject",
            "kelas",
            "fase",
            "status",
            "created_at",
            "updated_at",
        }
        sort_col = sort if sort in valid_sort_cols else "created_at"
        column = getattr(SchoolSubjectModel, sort_col)
        if order_by and str(order_by).lower() == "asc":
            stmt = stmt.order_by(asc(column))
        else:
            stmt = stmt.order_by(desc(column))

        if paginator:
            page = int(paginator.get("page", 1))
            limit = paginator.get("limit")
            if limit is not None and int(limit) > 0:
                limit = int(limit)
                offset = (page - 1) * limit
                stmt = stmt.offset(offset).limit(limit)

        return list(db.scalars(stmt).unique().all())

    def count_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(SchoolSubjectModel)
            .where(SchoolSubjectModel.deleted_at.is_(None))
        )

        if where:
            for k, v in where.items():
                if hasattr(SchoolSubjectModel, k) and v is not None and v != "":
                    stmt = stmt.where(getattr(SchoolSubjectModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    SchoolSubjectModel.name.ilike(kw),
                    SchoolSubjectModel.code_subject.ilike(kw),
                    SchoolSubjectModel.id_subject.ilike(kw),
                )
            )

        return db.scalar(stmt) or 0

    def find_by_id(self, db: Session, id: str) -> Optional[SchoolSubjectModel]:
        stmt = (
            select(SchoolSubjectModel)
            .options(
                joinedload(SchoolSubjectModel.category),
                joinedload(SchoolSubjectModel.major),
            )
            .where(
                SchoolSubjectModel.id_subject == id,
                SchoolSubjectModel.deleted_at.is_(None),
            )
        )
        return db.scalars(stmt).first()
