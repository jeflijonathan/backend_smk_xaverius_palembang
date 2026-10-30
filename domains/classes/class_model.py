import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base, engine
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class_student_association = Table(
    "class_student_association",
    Base.metadata,
    Column(
        "id_class",
        String(36),
        ForeignKey("classes.id_class", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_student",
        String(36),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


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
    id_school_information = Column(
        String(36), ForeignKey("school_informations.id_school_information", ondelete="CASCADE"), nullable=True
    )
    kelas = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)
    status = Column(Boolean, default=True, nullable=False)

    major = relationship("MajorModel", back_populates="classes")
    class_guardian = relationship(
        "EmployeeModel",
        foreign_keys=[id_class_guardian],
        back_populates="guardian_classes"
    )
    school_information = relationship(
        "SchoolInformationModel",
        foreign_keys=[id_school_information]
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
    students = relationship(
        "StudentModel",
        secondary=class_student_association,
        lazy="selectin",
    )


try:
    class_student_association.create(bind=engine, checkfirst=True)
except Exception:
    pass

