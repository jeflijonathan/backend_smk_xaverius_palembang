from typing import Any
from typing_extensions import Dict
from typing_extensions import Optional
from typing import List
from sqlalchemy.orm import Session
from domains.employee.employee_repository import EmployeeRepository
from domains.employee.dto.employee_schema import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepository()

    def get_all(self, db: Session, paginator: Optional[Dict[str, Any]] = None) -> List:
        return self.repo.find_all(db)
    
    def count_all(self, db: Session) -> int:
        return self.repo.count_all(db)

    def create_employee(self, db: Session, data: EmployeeCreate):
        user_data = data.user.dict()
        detail_data = data.detail.dict(exclude_unset=True) if data.detail else None
        return self.repo.create_employee(db, user_data, data.profile.dict(), detail_data)

    def update_employee(self, db: Session, id: str, data: EmployeeUpdate):
        profile_data = data.dict(exclude={'detail'}, exclude_unset=True)
        detail_data = data.detail.dict(exclude_unset=True) if data.detail else None
        return self.repo.update_employee(db, id, profile_data, detail_data)

    def delete_employee(self, db: Session, id: str):
        return self.repo.delete_employee(db, id)
