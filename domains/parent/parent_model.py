import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps

def generate_uuid():
    return str(uuid.uuid4())

class UserParentModel(Base, Timestamps):
    __tablename__ = "users_parents"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    profile = relationship(
        "ParentModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

student_parent_association = Table(
    "student_parent_association",
    Base.metadata,
    Column("student_id", String(36), ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("parent_id", String(36), ForeignKey("parents.id", ondelete="CASCADE"), primary_key=True),
)

class ParentModel(Base, Timestamps):
    __tablename__ = "parents"

    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    user_id = Column(String(36), ForeignKey(
        "users_parents.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(20), nullable=True)
    nik = Column(String(20), unique=True, nullable=True)
    occupation = Column(String(100), nullable=True)
    income = Column(String(50), nullable=True)

    user = relationship("UserParentModel", back_populates="profile")
    
    students = relationship(
        "StudentModel",
        secondary=student_parent_association,
        back_populates="parents"
    )
