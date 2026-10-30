import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


from domains.auth.role_model import RoleModel
from domains.auth.associations import user_roles_association


class UserModel(Base, Timestamps):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    roles = relationship(
        "RoleModel", secondary=user_roles_association, back_populates="users"
    )

    student_profile = relationship(
        "StudentModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    employee_profile = relationship(
        "EmployeeModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
