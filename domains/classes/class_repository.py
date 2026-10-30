from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, asc, desc, func
from common.base.baseMysql import BaseMySQLService
from domains.classes.class_model import ClassModel


class ClassRepository(BaseMySQLService[ClassModel]):
    def __init__(self):
        super().__init__(ClassModel)

    def find_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> List[ClassModel]:
        options = [
            joinedload(ClassModel.major),
            joinedload(ClassModel.class_guardian),
            joinedload(ClassModel.school_information),
        ]

        stmt = select(ClassModel)
        for opt in options:
            stmt = stmt.options(opt)

        if where:
            for k, v in where.items():
                if hasattr(ClassModel, k) and v is not None:
                    stmt = stmt.where(getattr(ClassModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    ClassModel.name.ilike(kw),
                    ClassModel.kelas.ilike(kw),
                )
            )

        valid_sort_cols = {"name", "kelas", "created_at", "status"}
        sort_col = sort if sort in valid_sort_cols else "created_at"
        column = getattr(ClassModel, sort_col)
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
        stmt = select(func.count()).select_from(ClassModel)

        if where:
            for k, v in where.items():
                if hasattr(ClassModel, k) and v is not None:
                    stmt = stmt.where(getattr(ClassModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    ClassModel.name.ilike(kw),
                    ClassModel.kelas.ilike(kw),
                )
            )

        return db.scalar(stmt) or 0

    def find_by_id(self, db: Session, id_class: str) -> Optional[ClassModel]:
        options = [
            joinedload(ClassModel.major),
            joinedload(ClassModel.class_guardian),
            joinedload(ClassModel.school_information),
        ]
        stmt = select(ClassModel).where(ClassModel.id_class == id_class)
        for opt in options:
            stmt = stmt.options(opt)
        return db.scalars(stmt).unique().first()

    def get_class_students(self, db: Session, id_class: str) -> List[Any]:
        cls_obj = self.find_by_id(db, id_class)
        if not cls_obj:
            return []
        return list(cls_obj.students)

    def add_students_to_class(
        self, db: Session, id_class: str, student_ids: List[str], force_transfer: bool = False
    ) -> List[Any]:
        cls_obj = self.find_by_id(db, id_class)
        if not cls_obj:
            raise ValueError(f"Class with id {id_class} not found")
        from domains.student.student_model import StudentModel
        from domains.classes.class_model import class_student_association, ClassModel
        from domains.schoolInformation.school_information_model import SchoolInformationModel

        # Cek apakah ada siswa yang sudah terdaftar di kelas lain DALAM PERIODE YANG SAMA
        # Jika beda periode, siswa diizinkan terdaftar (tidak dianggap konflik)
        period_filter = (
            ClassModel.id_school_information == cls_obj.id_school_information
            if cls_obj.id_school_information
            else ClassModel.id_school_information.is_(None)
        )

        assoc_rows = (
            db.query(
                class_student_association.c.id_student,
                ClassModel.name,
                ClassModel.kelas,
                ClassModel.id_class,
                SchoolInformationModel.periode,
            )
            .join(ClassModel, class_student_association.c.id_class == ClassModel.id_class)
            .outerjoin(
                SchoolInformationModel,
                ClassModel.id_school_information == SchoolInformationModel.id_school_information,
            )
            .filter(class_student_association.c.id_student.in_(student_ids))
            .filter(class_student_association.c.id_class != id_class)
            .filter(period_filter)
            .all()
        )

        if assoc_rows and not force_transfer:
            conflict_names = []
            for row in assoc_rows:
                student = db.query(StudentModel).filter(StudentModel.id == row.id_student).first()
                s_name = f"{student.first_name} {student.last_name or ''}".strip() if student else row.id_student
                c_name = row.name or f"Kelas {row.kelas}"
                periode_str = f" (Periode {row.periode})" if row.periode else ""
                conflict_names.append(f"{s_name} (di {c_name}{periode_str})")
            raise ValueError(
                f"Siswa berikut sudah terdaftar di kelas lain pada periode yang sama: {', '.join(conflict_names)}. Harap konfirmasi pemindahan kelas."
            )

        # Jika force_transfer=True, keluarkan siswa dari kelas sebelumnya HANYA pada periode yang sama
        if assoc_rows and force_transfer:
            conflicting_class_ids = list({row.id_class for row in assoc_rows})
            for row in assoc_rows:
                db.execute(
                    class_student_association.delete().where(
                        class_student_association.c.id_student == row.id_student,
                        class_student_association.c.id_class.in_(conflicting_class_ids),
                    )
                )

        students = db.query(StudentModel).filter(StudentModel.id.in_(student_ids)).all()
        for s in students:
            if s not in cls_obj.students:
                cls_obj.students.append(s)
        db.commit()
        db.refresh(cls_obj)
        return list(cls_obj.students)

    def remove_student_from_class(self, db: Session, id_class: str, student_id: str) -> bool:
        cls_obj = self.find_by_id(db, id_class)
        if not cls_obj:
            raise ValueError(f"Class with id {id_class} not found")
        from domains.student.student_model import StudentModel
        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if student and student in cls_obj.students:
            cls_obj.students.remove(student)
            db.commit()
            return True
        return False

    def get_available_students(self, db: Session, id_class: str) -> List[Dict[str, Any]]:
        cls_obj = self.find_by_id(db, id_class)
        if not cls_obj:
            return []

        current_student_ids = [s.id for s in cls_obj.students] if cls_obj else []
        from domains.student.student_model import StudentModel
        from domains.classes.class_model import class_student_association, ClassModel
        from domains.schoolInformation.school_information_model import SchoolInformationModel

        query = db.query(StudentModel)
        if current_student_ids:
            query = query.filter(~StudentModel.id.in_(current_student_ids))
        students = query.order_by(StudentModel.first_name.asc()).all()

        # Ambil pemetaan kelas siswa HANYA untuk periode yang sama dengan kelas target
        # Jika beda periode, siswa bebas didaftarkan (tidak ada konflik)
        period_filter = (
            ClassModel.id_school_information == cls_obj.id_school_information
            if cls_obj.id_school_information
            else ClassModel.id_school_information.is_(None)
        )

        assoc_rows = (
            db.query(
                class_student_association.c.id_student,
                ClassModel.id_class,
                ClassModel.name,
                ClassModel.kelas,
                SchoolInformationModel.periode,
            )
            .join(ClassModel, class_student_association.c.id_class == ClassModel.id_class)
            .outerjoin(
                SchoolInformationModel,
                ClassModel.id_school_information == SchoolInformationModel.id_school_information,
            )
            .filter(ClassModel.id_class != id_class)
            .filter(period_filter)
            .all()
        )

        student_class_map = {
            row.id_student: {
                "id_class": row.id_class,
                "name": row.name or f"Kelas {row.kelas}",
                "kelas": row.kelas,
                "periode": row.periode,
            }
            for row in assoc_rows
        }

        result = []
        for s in students:
            curr_class = student_class_map.get(s.id)
            result.append({
                "id": s.id,
                "nis": s.nis,
                "nisn": s.nisn,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "gender": s.gender,
                "email": s.email,
                "phone_number": s.phone_number,
                "profile_url": s.profile_url,
                "status": s.status,
                "current_class": curr_class,
            })
        return result

