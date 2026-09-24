from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.employee.employee_model import EmployeeModel, UserEmployeeModel, EmployeeDetailModel

class EmployeeRepository(BaseMySQLService[EmployeeModel]):
    def __init__(self):
        super().__init__(EmployeeModel)

    def find_all(
        self, 
        db: Session, 
        where: Optional[Dict[str, Any]] = None, 
        paginator: Optional[Dict[str, int]] = None
    ) -> List[EmployeeModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data, paginator)

    def count_all(self, db: Session) -> int:
        return self.count(db, {})   

    def find_by_id(self, db: Session, id: str) -> Optional[EmployeeModel]:
        return self.find_one(db, {"id": id})

    def create_employee(self, db: Session, user_data: Dict[str, Any], profile_data: Dict[str, Any], detail_data: Optional[Dict[str, Any]] = None) -> EmployeeModel:
        try:
            new_user = UserEmployeeModel(**user_data)
            db.add(new_user)
            db.flush()
            
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
        except Exception as e:
            db.rollback()
            raise e

    def update_employee(self, db: Session, employee_id: str, profile_data: Dict[str, Any], detail_data: Optional[Dict[str, Any]] = None) -> Optional[EmployeeModel]:
        try:
            employee = self.find_by_id(db, employee_id)
            if not employee:
                return None
            
            if profile_data:
                db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).update(profile_data)
            
            if detail_data:
                detail = db.query(EmployeeDetailModel).filter(EmployeeDetailModel.employee_id == employee_id).first()
                if detail:
                    db.query(EmployeeDetailModel).filter(EmployeeDetailModel.employee_id == employee_id).update(detail_data)
                else:
                    detail_data["employee_id"] = employee_id
                    new_detail = EmployeeDetailModel(**detail_data)
                    db.add(new_detail)
                
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
