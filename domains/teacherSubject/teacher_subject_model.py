import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class TeacherSubjectModel(Base, Timestamps):
    __tablename__ = "teacher_subjects"

    id_teacher_subject = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_teacher_subject")

    id_category_subject = Column(
        String(36),
        ForeignKey("category_subjects.id_category_subject", ondelete="CASCADE"),
        nullable=False,
    )
    id_subject = Column(
        String(36),
        ForeignKey("school_subjects.id_subject", ondelete="CASCADE"),
        nullable=False,
    )
    id_teacher = Column(
        String(36),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    jp_amount = Column(Integer, default=0, nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    category_subject = relationship(
        "CategorySubjectModel", back_populates="teacher_subjects"
    )
    subject = relationship(
        "SchoolSubjectModel", back_populates="teacher_subjects"
    )
    teacher = relationship(
        "EmployeeModel", foreign_keys=[id_teacher], back_populates="teacher_subjects"
    )
    classrooms = relationship(
        "ClassRoomModel",
        back_populates="teacher_subject",
        cascade="all, delete-orphan",
    )
