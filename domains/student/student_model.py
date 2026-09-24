from sqlalchemy.sql.sqltypes import Date
from sqlalchemy import Enum
import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps
from domains.auth.associations import student_roles_association
from domains.parent.parent_model import student_parent_association


def generate_uuid():
    return str(uuid.uuid4())


class UserStudentModel(Base, Timestamps):
    __tablename__ = "users_students"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    profile = relationship(
        "StudentModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class StudentModel(Base, Timestamps):
    __tablename__ = "students"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    user_id = Column(String(36), ForeignKey(
        "users_students.id", ondelete="CASCADE"), unique=True, nullable=False)
    nis = Column(String(100), unique=True, nullable=False, index=True)
    nisn = Column(String(100), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Enum("L", "P"), nullable=False)
    rt = Column(String(10), nullable=True)
    rw = Column(String(10), nullable=True)
    birth_place = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)
    zip_code = Column(String(5), nullable=True)
    address = Column(String(100), nullable=True)

    status = Column(Boolean, default=True, nullable=False)
    roles = relationship(
        "RoleModel", secondary=student_roles_association, back_populates="students"
    )
    user = relationship("UserStudentModel", back_populates="profile")
    
    parents = relationship(
        "ParentModel",
        secondary=student_parent_association,
        back_populates="students"
    )
    # classroom = relationship("ClassRoomModel", back_populates="StudentModel")
    # posts = relationship(
    #     "StudentPostModel", back_populates="student", cascade="all, delete-orphan"
    # )
