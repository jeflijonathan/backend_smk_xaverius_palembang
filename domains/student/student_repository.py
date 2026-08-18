from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.student.student_model import StudentModel, UserStudentModel

class StudentRepository(BaseMySQLService[StudentModel]):
    def __init__(self):
        super().__init__(StudentModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[StudentModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id: str) -> Optional[StudentModel]:
        return self.find_one(db, {"id": id})

    def find_user_by_username(self, db: Session, username: str) -> Optional[UserStudentModel]:
        return db.query(UserStudentModel).filter(UserStudentModel.username == username).first()

    def find_by_email(self, db: Session, email: str) -> Optional[StudentModel]:
        return self.find_one(db, {"email": email})

    def find_by_nis(self, db: Session, nis: str) -> Optional[StudentModel]:
        return self.find_one(db, {"nis": nis})

    def find_by_nisn(self, db: Session, nisn: str) -> Optional[StudentModel]:
        return self.find_one(db, {"nisn": nisn})

    def create_student(self, db: Session, user_data: Dict[str, Any], profile_data: Dict[str, Any]) -> StudentModel:
        try:
            # Create UserStudentModel first
            new_user = UserStudentModel(**user_data)
            db.add(new_user)
            db.flush() # flush to get new_user.id

            # Create StudentModel linked to UserStudentModel
            profile_data["user_id"] = new_user.id
            new_student = StudentModel(**profile_data)
            db.add(new_student)
            
            db.commit()
            db.refresh(new_student)
            return new_student
        except Exception as e:
            db.rollback()
            raise e

    def update_student(self, db: Session, student_id: str, user_data: Dict[str, Any], profile_data: Dict[str, Any]) -> Optional[StudentModel]:
        try:
            student = self.find_by_id(db, student_id)
            if not student:
                return None
            
            if user_data:
                db.query(UserStudentModel).filter(UserStudentModel.id == student.user_id).update(user_data)
            
            if profile_data:
                db.query(StudentModel).filter(StudentModel.id == student_id).update(profile_data)
                
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
            # This should also cascade delete StudentModel due to ForeignKey setup
            db.query(UserStudentModel).filter(UserStudentModel.id == user_id).delete()
            db.commit()
            return student
        except Exception as e:
            db.rollback()
            raise e
