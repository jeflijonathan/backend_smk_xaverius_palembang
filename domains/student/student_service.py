from typing import List, Optional
from sqlalchemy.orm import Session
from domains.student.student_model import StudentModel, UserStudentModel
from domains.student.student_repository import StudentRepository
from domains.student.dto.student_dto import CreateStudentDTO, UpdateStudentDTO

class StudentService:
    def __init__(self):
        self._student_repository = StudentRepository()

    def get_all_students(self, db: Session) -> List[StudentModel]:
        return self._student_repository.find_all(db)

    def get_student_by_id(self, db: Session, student_id: str) -> Optional[StudentModel]:
        return self._student_repository.find_by_id(db, student_id)

    def create_student(self, db: Session, student_data: CreateStudentDTO) -> StudentModel:
        if self._student_repository.find_user_by_username(db, student_data.username):
            raise ValueError("Username already registered!")
        
        if self._student_repository.find_by_email(db, student_data.email):
            raise ValueError("Email already registered!")
            
        if self._student_repository.find_by_nis(db, student_data.nis):
            raise ValueError("NIS already registered!")
            
        if self._student_repository.find_by_nisn(db, student_data.nisn):
            raise ValueError("NISN already registered!")

        user_data = {
            "username": student_data.username,
            "password": student_data.password 
        }
        
        profile_data = {
            "nis": student_data.nis,
            "nisn": student_data.nisn,
            "full_name": student_data.full_name,
            "email": student_data.email,
            "phone_number": student_data.phone_number,
            "description": student_data.description,
            "status": student_data.status
        }
        
        return self._student_repository.create_student(db, user_data, profile_data)

    def update_student(self, db: Session, student_id: str, update_data: UpdateStudentDTO) -> Optional[StudentModel]:
        clean_update_data = update_data.model_dump(exclude_unset=True)

        if not clean_update_data:
            return self._student_repository.find_by_id(db, student_id)
            
        student = self._student_repository.find_by_id(db, student_id)
        if not student:
            raise ValueError("Student not found!")

        if "username" in clean_update_data:
            existing_user = self._student_repository.find_user_by_username(db, clean_update_data["username"])
            if existing_user and existing_user.id != student.user_id:
                raise ValueError("Username already in use by another user!")
                
        if "email" in clean_update_data:
            existing_student = self._student_repository.find_by_email(db, clean_update_data["email"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("Email already in use by another student!")
                
        if "nis" in clean_update_data:
            existing_student = self._student_repository.find_by_nis(db, clean_update_data["nis"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("NIS already in use by another student!")
                
        if "nisn" in clean_update_data:
            existing_student = self._student_repository.find_by_nisn(db, clean_update_data["nisn"])
            if existing_student and existing_student.id != student_id:
                raise ValueError("NISN already in use by another student!")

        user_data = {}
        if "username" in clean_update_data:
            user_data["username"] = clean_update_data["username"]
        if "password" in clean_update_data:
            user_data["password"] = clean_update_data["password"]
            
        profile_data = {k: v for k, v in clean_update_data.items() if k not in ["username", "password"]}

        updated_student = self._student_repository.update_student(
            db, student_id, user_data, profile_data
        )

        return updated_student

    def delete_student(self, db: Session, student_id: str) -> Optional[StudentModel]:
        student = self._student_repository.find_by_id(db, student_id)
        if not student:
            raise ValueError("Student not found!")
        return self._student_repository.delete_student(db, student_id)
