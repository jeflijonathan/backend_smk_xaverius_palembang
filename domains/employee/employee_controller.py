from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from domains.employee.employee_service import EmployeeService
from domains.employee.dto.employee_schema import EmployeeCreate, EmployeeUpdate
from common.base.baseController import BaseController, PaginationParams

class EmployeeController(BaseController, prefix="/employees", tags=["Employees"]):
    _service = EmployeeService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_employees(pagination: PaginationParams = Depends(),db: Session = Depends(get_db)):
            try:
                paginator_dict = pagination.to_dict()
                employee = cls._service.get_all(db, paginator=paginator_dict)
                total_data = cls._service.count_all(db)

                return cls.handle_paginated_success(
                    data=employee,
                    total_data = total_data,
                    page=pagination.page,
                    limit=pagination.limit,
                    message="Employees retrieved successfully",
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
            try:
                employee = cls._service.create_employee(db, data)
                return cls.handle_success(
                    data=employee,
                    message="Employee created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.patch("/{id}", status_code=status.HTTP_200_OK)
        def update_employee(id: str, data: EmployeeUpdate, db: Session = Depends(get_db)):
            try:
                employee = cls._service.update_employee(db, id, data)
                if not employee:
                    cls.handle_error(
                        detail=f"Employee with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=employee, message="Employee updated successfully"
                )
            except ValueError as error:
                cls.handle_error(detail=str(error), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.delete("/{id}", status_code=status.HTTP_200_OK)
        def delete_employee(id: str, db: Session = Depends(get_db)):
            try:
                employee = cls._service.delete_employee(db, id)
                if not employee:
                    cls.handle_error(
                        detail=f"Employee with id {id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=employee, message="Employee deleted successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


EmployeeController.register_routes()
router = EmployeeController.get_router()
