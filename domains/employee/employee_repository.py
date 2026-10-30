from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.employee.employee_model import EmployeeModel, EmployeeDetailModel
from domains.users.user_model import UserModel
from domains.auth.role_model import RoleModel

class EmployeeRepository(BaseMySQLService[EmployeeModel]):
    def __init__(self):
        super().__init__(EmployeeModel)

    def find_all(
        self, 
        db: Session, 
        where: Optional[Dict[str, Any]] = None, 
        paginator: Optional[Dict[str, int]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> List[EmployeeModel]:
        from sqlalchemy import select, asc, desc

        options = [
            joinedload(EmployeeModel.user).joinedload(UserModel.roles),
            joinedload(EmployeeModel.detail)
        ]

        stmt = select(EmployeeModel)
        for opt in options:
            stmt = stmt.options(opt)

        # Filter berdasarkan where dict
        if where:
            for k, v in where.items():
                if hasattr(EmployeeModel, k) and v is not None:
                    stmt = stmt.where(getattr(EmployeeModel, k) == v)

        # Pencarian teks (LIKE)
        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    EmployeeModel.first_name.ilike(kw),
                    EmployeeModel.last_name.ilike(kw),
                    EmployeeModel.niy.ilike(kw),
                    EmployeeModel.email.ilike(kw),
                )
            )

        # Sorting
        valid_sort_cols = {"first_name", "last_name", "niy", "email", "created_at", "status"}
        sort_col = sort if sort in valid_sort_cols else "created_at"
        column = getattr(EmployeeModel, sort_col)
        if order_by and str(order_by).lower() == "asc":
            stmt = stmt.order_by(asc(column))
        else:
            stmt = stmt.order_by(desc(column))

        # Pagination
        if paginator:
            page = int(paginator.get("page", 1))
            limit = paginator.get("limit")
            if limit is not None and int(limit) > 0:
                limit = int(limit)
                offset = (page - 1) * limit
                stmt = stmt.offset(offset).limit(limit)

        return list(db.scalars(stmt).unique().all())

    def count_all(self, db: Session, search: Optional[str] = None) -> int:
        from sqlalchemy import select, func
        stmt = select(func.count()).select_from(EmployeeModel)
        if search and search.strip():
            kw = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    EmployeeModel.first_name.ilike(kw),
                    EmployeeModel.last_name.ilike(kw),
                    EmployeeModel.niy.ilike(kw),
                    EmployeeModel.email.ilike(kw),
                )
            )
        return db.scalar(stmt) or 0

    def find_by_id(self, db: Session, id: str) -> Optional[EmployeeModel]:
        options = [
            joinedload(EmployeeModel.user).joinedload(UserModel.roles),
            joinedload(EmployeeModel.detail)
        ]
        return self.find_one(db, {"id": id}, options)

    def create_employee(self, db: Session, user_data: Dict[str, Any], profile_data: Dict[str, Any], detail_data: Optional[Dict[str, Any]] = None, role_ids: List[str] = None) -> EmployeeModel:
        try:
            # Validasi duplikat sebelum insert
            existing_user = db.query(UserModel).filter(
                UserModel.username == user_data.get("username"),
                UserModel.deleted_at == None
            ).first()
            if existing_user:
                raise ValueError(f"Username '{user_data['username']}' sudah digunakan")
            
            existing_niy = db.query(EmployeeModel).filter(
                EmployeeModel.niy == profile_data.get("niy"),
                EmployeeModel.deleted_at == None
            ).first()
            if existing_niy:
                raise ValueError(f"NIY '{profile_data['niy']}' sudah digunakan")
            
            existing_email = db.query(EmployeeModel).filter(
                EmployeeModel.email == profile_data.get("email"),
                EmployeeModel.deleted_at == None
            ).first()
            if existing_email:
                raise ValueError(f"Email '{profile_data['email']}' sudah digunakan")
            
            # Buat UserModel terlebih dahulu
            new_user = UserModel(**user_data)
            db.add(new_user)
            db.flush()
            
            # Assign roles ke user
            if role_ids:
                roles = db.query(RoleModel).filter(RoleModel.id.in_(role_ids)).all()
                if len(roles) != len(role_ids):
                    found_ids = {r.id for r in roles}
                    missing = [rid for rid in role_ids if rid not in found_ids]
                    raise ValueError(f"Role IDs tidak ditemukan: {missing}")
                new_user.roles = roles
                db.flush()
            
            # Buat EmployeeModel yang terhubung ke UserModel
            profile_data["user_id"] = new_user.id
            new_employee = EmployeeModel(**profile_data)
            db.add(new_employee)
            db.flush()
            
            if detail_data:
                detail_data["employee_id"] = new_employee.id
                new_detail = EmployeeDetailModel(**detail_data)
                db.add(new_detail)
            
            db.commit()
            db.refresh(new_employee)
            return new_employee
        except ValueError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise e

    def update_employee(self, db: Session, employee_id: str, user_data: Dict[str, Any] = None, profile_data: Dict[str, Any] = None, detail_data: Optional[Dict[str, Any]] = None, role_ids: Optional[List[str]] = None) -> Optional[EmployeeModel]:
        try:
            employee = self.find_by_id(db, employee_id)
            if not employee:
                return None
            
            user = employee.user
            if not user and employee.user_id:
                user = db.query(UserModel).filter(UserModel.id == employee.user_id).first()

            if user_data:
                if "username" in user_data and user_data["username"]:
                    username_val = str(user_data["username"]).strip()
                    existing_user = db.query(UserModel).filter(
                        UserModel.username == username_val,
                        UserModel.id != employee.user_id,
                        UserModel.deleted_at == None
                    ).first()
                    if existing_user:
                        raise ValueError(f"Username '{username_val}' sudah digunakan")
                    user_data["username"] = username_val
                
                if user:
                    for k, v in user_data.items():
                        setattr(user, k, v)
                    db.add(user)
            
            if profile_data:
                if "niy" in profile_data and profile_data["niy"]:
                    existing_niy = db.query(EmployeeModel).filter(
                        EmployeeModel.niy == profile_data["niy"],
                        EmployeeModel.id != employee_id,
                        EmployeeModel.deleted_at == None
                    ).first()
                    if existing_niy:
                        raise ValueError(f"NIY '{profile_data['niy']}' sudah digunakan")

                if "email" in profile_data and profile_data["email"]:
                    existing_email = db.query(EmployeeModel).filter(
                        EmployeeModel.email == profile_data["email"],
                        EmployeeModel.id != employee_id,
                        EmployeeModel.deleted_at == None
                    ).first()
                    if existing_email:
                        raise ValueError(f"Email '{profile_data['email']}' sudah digunakan")
                
                for k, v in profile_data.items():
                    setattr(employee, k, v)
                db.add(employee)

            # Sinkronisasi full_name pada UserModel jika nama depan / belakang berubah
            if user:
                first = profile_data.get("first_name", employee.first_name) if profile_data else employee.first_name
                last = profile_data.get("last_name", employee.last_name) if profile_data else employee.last_name
                user.full_name = f"{first} {last or ''}".strip()
                db.add(user)
            
            # Update roles jika diberikan
            if role_ids is not None and user:
                roles = db.query(RoleModel).filter(RoleModel.id.in_(role_ids)).all()
                user.roles = roles
                db.add(user)
            
            if detail_data:
                detail = employee.detail or db.query(EmployeeDetailModel).filter(EmployeeDetailModel.employee_id == employee_id).first()
                if detail:
                    for k, v in detail_data.items():
                        setattr(detail, k, v)
                    db.add(detail)
                else:
                    detail_data["employee_id"] = employee_id
                    new_detail = EmployeeDetailModel(**detail_data)
                    db.add(new_detail)
                    employee.detail = new_detail
                
            db.commit()
            db.expire_all()
            return self.find_by_id(db, employee_id)
        except ValueError:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise e

    def delete_employee(self, db: Session, employee_id: str):
        try:
            employee = self.find_by_id(db, employee_id)
            if not employee:
                return None
            
            # Cascade delete: menghapus UserModel akan otomatis menghapus EmployeeModel
            db.query(UserModel).filter(UserModel.id == employee.user_id).delete()
            db.commit()
            return employee
        except Exception as e:
            db.rollback()
            raise e
