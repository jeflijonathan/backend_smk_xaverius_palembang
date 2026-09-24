import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class ClassModel(Base, Timestamps):
    __tablename__ = "classes"

    id_class = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    id = synonym("id_class")

    id_major = Column(
        String(36), ForeignKey("majors.id_major", ondelete="CASCADE"), nullable=False
    )
    id_class_guardian = Column(
        String(36), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    major = relationship("MajorModel", back_populates="classes")
    class_guardian = relationship(
        "EmployeeModel",
        foreign_keys=[id_class_guardian],
        back_populates="guardian_classes"
    )
    classrooms = relationship(
        "ClassRoomModel",
        back_populates="class_",
        cascade="all, delete-orphan"
    )
    schedules = relationship(
        "ScheduleModel",
        back_populates="class_",
        cascade="all, delete-orphan"
    )
