import os
import shutil
from typing import List, Optional
from sqlalchemy.orm import Session
from domains.student.student_model import StudentModel
from domains.student.student_repository import StudentRepository
from domains.student.dto.student_dto import CreateStudentDTO, UpdateStudentDTO
from domains.uploadFile.upload_file_model import UploadFileModel


class StudentService:
    def __init__(self):
        self._student_repository = StudentRepository()

    def get_all_students(
        self,
        db: Session,
        where: Optional[dict] = None,
        paginator: Optional[dict] = None,
    ) -> List[StudentModel]:
        search = paginator.get("value") if paginator else None
        sort = paginator.get("sort") if paginator else None
        order_by = paginator.get("order_by") if paginator else None
        return self._student_repository.find_all(
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
        where: Optional[dict] = None,
        search: Optional[str] = None,
    ) -> int:
        return self._student_repository.count_all(db, where=where, search=search)

    def get_student_by_id(self, db: Session, student_id: str) -> Optional[StudentModel]:
        return self._student_repository.find_by_id(db, student_id)

    def _process_profile_image(self, db: Session, file_id: str):
        file_record = db.query(UploadFileModel).filter(UploadFileModel.id == file_id).first()
        if not file_record:
            return
        
        valid_mimes = ["image/jpeg", "image/jpg", "image/png"]
        if file_record.mime_type not in valid_mimes:
            raise ValueError("Uploaded file is not a valid image (jpg/jpeg/png).")
            
        if "uploads/temp" in file_record.file_url or "uploads\\temp" in file_record.file_url:
            dest_dir = "uploads/student"
            os.makedirs(dest_dir, exist_ok=True)
            filename = os.path.basename(file_record.file_url)
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                if os.path.exists(file_record.file_url):
                    shutil.move(file_record.file_url, dest_path)
                    file_record.file_url = dest_path.replace("\\", "/")
                    db.commit()
            except Exception:
                pass

    def _delete_profile_image(self, db: Session, file_id: str):
        file_record = db.query(UploadFileModel).filter(UploadFileModel.id == file_id).first()
        if file_record:
            if file_record.file_url and os.path.exists(file_record.file_url):
                try:
                    os.remove(file_record.file_url)
                except Exception:
                    pass
            db.delete(file_record)
            db.commit()

    def create_student(self, db: Session, student_data: CreateStudentDTO) -> StudentModel:
        username = student_data.username or student_data.nis
        if self._student_repository.find_user_by_username(db, username):
            raise ValueError(f"Username / NIS '{username}' sudah terdaftar!")

        if self._student_repository.find_by_nis(db, student_data.nis):
            raise ValueError(f"NIS '{student_data.nis}' sudah terdaftar!")

        if self._student_repository.find_by_nisn(db, student_data.nisn):
            raise ValueError(f"NISN '{student_data.nisn}' sudah terdaftar!")

        if student_data.email:
            existing_email = self._student_repository.find_by_email(db, str(student_data.email).strip())
            if existing_email:
                raise ValueError(f"Email '{student_data.email}' sudah terdaftar!")

        full_name = f"{student_data.first_name} {student_data.last_name}".strip()
        user_data = {
            "username": username,
            "password": student_data.password,
            "full_name": full_name,
            "status": student_data.status,
        }

        profile_data = {
            "nis": student_data.nis,
            "nisn": student_data.nisn,
            "first_name": student_data.first_name,
            "last_name": student_data.last_name,
            "email": str(student_data.email).strip() if student_data.email else None,
            "phone_number": str(student_data.phone_number).strip() if student_data.phone_number else None,
            "gender": student_data.gender if student_data.gender in ("L", "P") else "L",
            "birth_place": student_data.birth_place or None,
            "birth_date": student_data.birth_date or None,
            "address": student_data.address or None,
            "rt": student_data.rt or None,
            "rw": student_data.rw or None,
            "zip_code": student_data.zip_code or None,
            "profile_url": student_data.profile_url or None,
            "status": student_data.status,
        }

        # Kumpulkan data orang tua
        parents_data = []
        if student_data.parents:
            for p in student_data.parents:
                if p and p.name:
                    parents_data.append(p.model_dump())
        if student_data.parent and student_data.parent.name:
            parents_data.append(student_data.parent.model_dump())
        elif student_data.parent_name and student_data.parent_name.strip():
            parents_data.append({
                "name": student_data.parent_name.strip(),
                "nik": student_data.parent_nik.strip() if student_data.parent_nik else None,
                "phone_number": student_data.parent_phone_number.strip() if student_data.parent_phone_number else None,
                "email": student_data.parent_email if student_data.parent_email else None,
                "occupation": student_data.parent_occupation.strip() if student_data.parent_occupation else None,
                "income": student_data.parent_income.strip() if student_data.parent_income else None,
            })

        if student_data.mother and student_data.mother.name:
            parents_data.append(student_data.mother.model_dump())
        elif student_data.mother_name and student_data.mother_name.strip():
            parents_data.append({
                "name": student_data.mother_name.strip(),
                "nik": student_data.mother_nik.strip() if student_data.mother_nik else None,
                "phone_number": student_data.mother_phone_number.strip() if student_data.mother_phone_number else None,
                "email": student_data.mother_email if student_data.mother_email else None,
                "occupation": student_data.mother_occupation.strip() if student_data.mother_occupation else None,
                "income": student_data.mother_income.strip() if student_data.mother_income else None,
            })

        if student_data.profile_url:
            self._process_profile_image(db, student_data.profile_url)

        return self._student_repository.create_student(
            db,
            user_data,
            profile_data,
            role_ids=student_data.role_ids,
            parents_data=parents_data,
        )

    def update_student(self, db: Session, student_id: str, update_data: UpdateStudentDTO) -> Optional[StudentModel]:
        clean_update_data = update_data.model_dump(exclude_unset=True)

        if not clean_update_data:
            return self._student_repository.find_by_id(db, student_id)

        student = self._student_repository.find_by_id(db, student_id)
        if not student:
            raise ValueError("Student not found!")

        if "username" in clean_update_data and clean_update_data["username"]:
            existing_user = self._student_repository.find_user_by_username(db, clean_update_data["username"])
            if existing_user and existing_user.id != student.user_id:
                raise ValueError("Username already in use by another user!")

        if "nis" in clean_update_data and clean_update_data["nis"]:
            existing_student = self._student_repository.find_by_nis(db, clean_update_data["nis"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("NIS already in use by another student!")

        if "nisn" in clean_update_data and clean_update_data["nisn"]:
            existing_student = self._student_repository.find_by_nisn(db, clean_update_data["nisn"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("NISN already in use by another student!")

        if "email" in clean_update_data and clean_update_data["email"]:
            existing_student = self._student_repository.find_by_email(db, clean_update_data["email"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("Email already in use by another student!")

        user_fields = {"username", "password", "status"}
        user_data = {k: v for k, v in clean_update_data.items() if k in user_fields and v is not None}

        first_name = clean_update_data.get("first_name", student.first_name)
        last_name = clean_update_data.get("last_name", student.last_name)
        if "first_name" in clean_update_data or "last_name" in clean_update_data:
            user_data["full_name"] = f"{first_name} {last_name}".strip()

        valid_student_cols = {
            "nis", "nisn", "first_name", "last_name", "gender",
            "rt", "rw", "birth_place", "birth_date", "zip_code",
            "address", "status", "email", "phone_number", "profile_url"
        }
        profile_data = {k: v for k, v in clean_update_data.items() if k in valid_student_cols}

        if "profile_url" in clean_update_data:
            new_profile_id = clean_update_data.get("profile_url")
            old_profile_id = student.profile_url
            if new_profile_id and new_profile_id != old_profile_id:
                self._process_profile_image(db, new_profile_id)
                if old_profile_id:
                    self._delete_profile_image(db, old_profile_id)
            elif not new_profile_id and old_profile_id:
                self._delete_profile_image(db, old_profile_id)
                profile_data["profile_url"] = None

        role_ids = clean_update_data.get("role_ids")

        parents_data = None
        p_items = []
        if update_data.parent_name and update_data.parent_name.strip():
            p_items.append({
                "name": update_data.parent_name.strip(),
                "nik": update_data.parent_nik.strip() if update_data.parent_nik else None,
                "phone_number": update_data.parent_phone_number.strip() if update_data.parent_phone_number else None,
                "email": update_data.parent_email if update_data.parent_email else None,
                "occupation": update_data.parent_occupation.strip() if update_data.parent_occupation else None,
                "income": update_data.parent_income.strip() if update_data.parent_income else None,
            })
        if update_data.mother_name and update_data.mother_name.strip():
            p_items.append({
                "name": update_data.mother_name.strip(),
                "nik": update_data.mother_nik.strip() if update_data.mother_nik else None,
                "phone_number": update_data.mother_phone_number.strip() if update_data.mother_phone_number else None,
                "email": update_data.mother_email if update_data.mother_email else None,
                "occupation": update_data.mother_occupation.strip() if update_data.mother_occupation else None,
                "income": update_data.mother_income.strip() if update_data.mother_income else None,
            })
        if p_items:
            parents_data = p_items

        return self._student_repository.update_student(
            db,
            student_id,
            user_data=user_data or None,
            profile_data=profile_data or None,
            role_ids=role_ids,
            parents_data=parents_data,
        )

    def delete_student(self, db: Session, student_id: str) -> Optional[StudentModel]:
        student = self._student_repository.find_by_id(db, student_id)
        if not student:
            raise ValueError("Student not found!")
        if student.profile_url:
            self._delete_profile_image(db, student.profile_url)
        return self._student_repository.delete_student(db, student_id)
