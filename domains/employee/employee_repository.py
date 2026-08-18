from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.employee.employee_model import EmployeeModel, UserEmployeeModel

class EmployeeRepository(BaseMySQLService[EmployeeModel]):
    def __init__(self):
        super().__init__(EmployeeModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[EmployeeModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id: str) -> Optional[EmployeeModel]:
        return self.find_one(db, {"id": id})

    def create_employee(self, db: Session, user_data: Dict[str, Any], profile_data: Dict[str, Any]) -> EmployeeModel:
        try:
            new_user = UserEmployeeModel(**user_data)
            db.add(new_user)
            db.flush()
            
            profile_data["user_id"] = new_user.id
            new_employee = EmployeeModel(**profile_data)
            db.add(new_employee)
            
            db.commit()
            db.refresh(new_employee)
            return new_employee
        except Exception as e:
            db.rollback()
            raise e

    def update_employee(self, db: Session, employee_id: str, profile_data: Dict[str, Any]) -> Optional[EmployeeModel]:
        try:
            employee = self.find_by_id(db, employee_id)
            if not employee:
                return None
            
            if profile_data:
                db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).update(profile_data)
                
            db.commit()
            db.refresh(employee)
            return employee
        except Exception as e:
            db.rollback()
            raise e

    def delete_employee(self, db: Session, employee_id: str):
        try:
            employee = self.find_by_id(db, employee_id)
            if not employee:
                return None
            
            db.query(UserEmployeeModel).filter(UserEmployeeModel.id == employee.user_id).delete()
            db.commit()
            return employee
        except Exception as e:
            db.rollback()
            raise e
