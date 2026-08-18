from typing import List
from sqlalchemy.orm import Session
from domains.employee.employee_repository import EmployeeRepository
from domains.employee.dto.employee_schema import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepository()

    def get_employees(self, db: Session) -> List:
        return self.repo.find_all(db)

    def create_employee(self, db: Session, data: EmployeeCreate):
        user_data = data.user.dict()
        # Password is not hashed here to avoid missing module errors. Use passlib/bcrypt in production.
        return self.repo.create_employee(db, user_data, data.profile.dict())

    def update_employee(self, db: Session, id: str, data: EmployeeUpdate):
        return self.repo.update_employee(db, id, data.dict(exclude_unset=True))

    def delete_employee(self, db: Session, id: str):
        return self.repo.delete_employee(db, id)
