import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, or_, func, asc, desc
from common.base.baseMysql import BaseMySQLService
from domains.student.student_model import StudentModel
from domains.users.user_model import UserModel
from domains.auth.role_model import RoleModel
from domains.parent.parent_model import ParentModel, UserParentModel

VALID_STUDENT_ROLES = {"siswa", "pengurus_kelas"}


class StudentRepository(BaseMySQLService[StudentModel]):
    def __init__(self):
        super().__init__(StudentModel)

    def find_all(
        self,
        db: Session,
        where: Optional[Dict[str, Any]] = None,
        paginator: Optional[Dict[str, int]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> List[StudentModel]:
        stmt = select(StudentModel).options(
            joinedload(StudentModel.user).joinedload(UserModel.roles),
            selectinload(StudentModel.parents),
        )

        if where:
            for k, v in where.items():
                if hasattr(StudentModel, k) and v is not None:
                    stmt = stmt.where(getattr(StudentModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    StudentModel.first_name.ilike(kw),
                    StudentModel.last_name.ilike(kw),
                    StudentModel.nis.ilike(kw),
                    StudentModel.nisn.ilike(kw),
                    StudentModel.email.ilike(kw),
                )
            )

        valid_sort_cols = {"first_name", "last_name", "nis", "nisn", "created_at", "status"}
        sort_col = sort if sort in valid_sort_cols else "created_at"
        column = getattr(StudentModel, sort_col)
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
        stmt = select(func.count()).select_from(StudentModel)

        if where:
            for k, v in where.items():
                if hasattr(StudentModel, k) and v is not None:
                    stmt = stmt.where(getattr(StudentModel, k) == v)

        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    StudentModel.first_name.ilike(kw),
                    StudentModel.last_name.ilike(kw),
                    StudentModel.nis.ilike(kw),
                    StudentModel.nisn.ilike(kw),
                    StudentModel.email.ilike(kw),
                )
            )

        return db.scalar(stmt) or 0

    def find_by_id(self, db: Session, id: str) -> Optional[StudentModel]:
        stmt = select(StudentModel).options(
            joinedload(StudentModel.user).joinedload(UserModel.roles),
            selectinload(StudentModel.parents),
        ).where(StudentModel.id == id)
        return db.scalars(stmt).first()

    def find_user_by_username(self, db: Session, username: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.username == username).first()

    def find_by_email(self, db: Session, email: str) -> Optional[StudentModel]:
        return self.find_one(db, {"email": email})

    def find_by_nis(self, db: Session, nis: str) -> Optional[StudentModel]:
        return self.find_one(db, {"nis": nis})

    def find_by_nisn(self, db: Session, nisn: str) -> Optional[StudentModel]:
        return self.find_one(db, {"nisn": nisn})

    def get_roles_by_ids_or_names(self, db: Session, role_ids: Optional[List[str]]) -> List[RoleModel]:
        """Ambil roles yang valid untuk siswa ('siswa', 'pengurus_kelas')."""
        if not role_ids:
            # Default ke role 'siswa'
            default_role = db.query(RoleModel).filter(RoleModel.name == "siswa").first()
            return [default_role] if default_role else []

        roles = db.query(RoleModel).filter(
            or_(RoleModel.id.in_(role_ids), RoleModel.name.in_(role_ids))
        ).all()

        # Validasi bahwa hanya role siswa atau pengurus_kelas yang diperbolehkan
        invalid_roles = [r.name for r in roles if r.name not in VALID_STUDENT_ROLES]
        if invalid_roles:
            raise ValueError(f"Role tidak valid untuk siswa: {invalid_roles}. Pilihan hanya 'siswa' dan 'pengurus_kelas'.")

        return roles

    def create_student(
        self,
        db: Session,
        user_data: Dict[str, Any],
        profile_data: Dict[str, Any],
        role_ids: Optional[List[str]] = None,
        parents_data: Optional[List[Dict[str, Any]]] = None,
    ) -> StudentModel:
        try:
            # 1. Buat UserModel
            new_user = UserModel(**user_data)
            db.add(new_user)
            db.flush()

            # Assign roles ke user siswa
            roles = self.get_roles_by_ids_or_names(db, role_ids)
            if roles:
                new_user.roles = roles
                db.flush()

            # 2. Buat StudentModel yang terhubung ke UserModel
            profile_data["user_id"] = new_user.id
            new_student = StudentModel(**profile_data)
            db.add(new_student)
            db.flush()

            # 3. Proses Data Orang Tua / Parent
            if parents_data:
                for p_dict in parents_data:
                    p_name = p_dict.get("name")
                    if not p_name or not str(p_name).strip():
                        continue

                    p_nik = str(p_dict["nik"]).strip() if p_dict.get("nik") else None
                    p_email = str(p_dict["email"]).strip() if p_dict.get("email") else None
                    p_phone = str(p_dict["phone_number"]).strip() if p_dict.get("phone_number") else None
                    p_occ = str(p_dict["occupation"]).strip() if p_dict.get("occupation") else None
                    p_inc = str(p_dict["income"]).strip() if p_dict.get("income") else None

                    existing_parent = None
                    if p_nik:
                        existing_parent = db.query(ParentModel).filter(ParentModel.nik == p_nik).first()
                    if not existing_parent and p_email:
                        existing_parent = db.query(ParentModel).filter(ParentModel.email == p_email).first()

                    if existing_parent:
                        if existing_parent not in new_student.parents:
                            new_student.parents.append(existing_parent)
                    else:
                        parent_username = p_nik or p_email or f"parent_{uuid.uuid4().hex[:10]}"
                        while db.query(UserParentModel).filter(UserParentModel.username == parent_username).first():
                            parent_username = f"parent_{uuid.uuid4().hex[:10]}"

                        parent_user = UserParentModel(
                            username=parent_username,
                            password=user_data.get("password", "password123"),
                        )
                        db.add(parent_user)
                        db.flush()

                        parent_obj = ParentModel(
                            user_id=parent_user.id,
                            name=str(p_name).strip(),
                            email=p_email,
                            phone_number=p_phone,
                            nik=p_nik,
                            occupation=p_occ,
                            income=p_inc,
                        )
                        db.add(parent_obj)
                        db.flush()

                        new_student.parents.append(parent_obj)

            db.commit()
            db.refresh(new_student)
            return new_student
        except Exception as e:
            db.rollback()
            raise e

    def update_student(
        self,
        db: Session,
        student_id: str,
        user_data: Optional[Dict[str, Any]] = None,
        profile_data: Optional[Dict[str, Any]] = None,
        role_ids: Optional[List[str]] = None,
        parents_data: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[StudentModel]:
        try:
            student = self.find_by_id(db, student_id)
            if not student:
                return None

            user = student.user
            if not user and student.user_id:
                user = db.query(UserModel).filter(UserModel.id == student.user_id).first()

            if user_data and user:
                db.query(UserModel).filter(UserModel.id == student.user_id).update(user_data)

            if role_ids is not None and user:
                roles = self.get_roles_by_ids_or_names(db, role_ids)
                user.roles = roles
                db.flush()

            if profile_data:
                db.query(StudentModel).filter(StudentModel.id == student_id).update(profile_data)

            # Update / Add parents
            if parents_data is not None:
                for p_dict in parents_data:
                    p_name = p_dict.get("name")
                    if not p_name or not str(p_name).strip():
                        continue

                    p_nik = str(p_dict["nik"]).strip() if p_dict.get("nik") else None
                    p_email = str(p_dict["email"]).strip() if p_dict.get("email") else None
                    p_phone = str(p_dict["phone_number"]).strip() if p_dict.get("phone_number") else None
                    p_occ = str(p_dict["occupation"]).strip() if p_dict.get("occupation") else None
                    p_inc = str(p_dict["income"]).strip() if p_dict.get("income") else None

                    existing_parent = None
                    if p_nik:
                        existing_parent = db.query(ParentModel).filter(ParentModel.nik == p_nik).first()
                    if not existing_parent and p_email:
                        existing_parent = db.query(ParentModel).filter(ParentModel.email == p_email).first()

                    if existing_parent:
                        if existing_parent not in student.parents:
                            student.parents.append(existing_parent)
                    else:
                        parent_username = p_nik or p_email or f"parent_{uuid.uuid4().hex[:10]}"
                        while db.query(UserParentModel).filter(UserParentModel.username == parent_username).first():
                            parent_username = f"parent_{uuid.uuid4().hex[:10]}"

                        parent_user = UserParentModel(
                            username=parent_username,
                            password="password123",
                        )
                        db.add(parent_user)
                        db.flush()

                        parent_obj = ParentModel(
                            user_id=parent_user.id,
                            name=str(p_name).strip(),
                            email=p_email,
                            phone_number=p_phone,
                            nik=p_nik,
                            occupation=p_occ,
                            income=p_inc,
                        )
                        db.add(parent_obj)
                        db.flush()

                        student.parents.append(parent_obj)

            db.commit()
            db.refresh(student)
            return student
        except Exception as e:
            db.rollback()
            raise e

    def delete_student(self, db: Session, student_id: str) -> Optional[StudentModel]:
        try:
            student = self.find_by_id(db, student_id)
            if not student:
                return None

            user_id = student.user_id
            db.query(UserModel).filter(UserModel.id == user_id).delete()
            db.commit()
            return student
        except Exception as e:
            db.rollback()
            raise e
