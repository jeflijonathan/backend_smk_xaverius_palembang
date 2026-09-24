import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class SchoolSubjectModel(Base, Timestamps):
    __tablename__ = "school_subjects"

    id_subject = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    id = synonym("id_subject")

    id_category_subject = Column(
        String(36), ForeignKey("category_subjects.id_category_subject", ondelete="CASCADE"), nullable=False
    )
    category_subject_id = synonym("id_category_subject")

    id_major = Column(
        String(36), ForeignKey("majors.id_major", ondelete="SET NULL"), nullable=True
    )

    code_subject = Column(String(50), nullable=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    category = relationship("CategorySubjectModel", back_populates="subjects")
    major = relationship("MajorModel", back_populates="subjects")
    teacher_subjects = relationship(
        "TeacherSubjectModel",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
    effective_weeks = relationship(
        "EffectiveWeekModel",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
