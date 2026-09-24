import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps
from domains.auth.associations import employee_roles_association


def generate_uuid():
    return str(uuid.uuid4())


class UserEmployeeModel(Base, Timestamps):
    __tablename__ = "users_employees"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    profile = relationship(
        "EmployeeModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class EmployeeDetailModel(Base, Timestamps):
    __tablename__ = "employee_details"
    
    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    gender = Column(String(10), nullable=True)
    birth_place = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    address = Column(Text, nullable=True)
    RT = Column(String(10), nullable=True)
    RW = Column(String(10), nullable=True)
    zip_code = Column(String(20), nullable=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    
    employee = relationship("EmployeeModel", back_populates="detail")


class EmployeeModel(Base, Timestamps):
    __tablename__ = "employees"
    
    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)

    user_id = Column(String(36), ForeignKey("users_employees.id", ondelete="CASCADE"), unique=True, nullable=False)

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    profile_url = Column(String(255), nullable=True)
    niy = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    status = Column(Boolean, default=True, nullable=False)

    roles = relationship(
        "RoleModel", secondary=employee_roles_association, back_populates="employees"
    )

    user = relationship("UserEmployeeModel", back_populates="profile")
    
    detail = relationship(
        "EmployeeDetailModel", 
        back_populates="employee", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    headmaster_schools = relationship(
        "SchoolInformationModel",
        back_populates="headmaster"
    )
    guardian_classes = relationship(
        "ClassModel",
        back_populates="class_guardian"
    )
    teacher_subjects = relationship(
        "TeacherSubjectModel",
        back_populates="teacher"
    )
    duty_schedules = relationship(
        "ScheduleModel",
        back_populates="duty_teacher"
    )
