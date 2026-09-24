import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class CategoryScheduleTimeModel(Base, Timestamps):
    __tablename__ = "category_schedule_times"

    id_category_schendule_time = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_category_schendule_time")

    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    schedule_times = relationship(
        "ScheduleTimeModel",
        back_populates="category_schedule_time",
        cascade="all, delete-orphan",
    )


class ScheduleTimeModel(Base, Timestamps):
    __tablename__ = "schedule_times"

    id_schendule_time = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_schendule_time")

    hari = Column(String(50), nullable=False)
    jam_awal = Column(String(10), nullable=False)
    jam_akhir = Column(String(10), nullable=False)
    id_category_schendule_time = Column(
        String(36),
        ForeignKey(
            "category_schedule_times.id_category_schendule_time", ondelete="CASCADE"
        ),
        nullable=False,
    )

    category_schedule_time = relationship(
        "CategoryScheduleTimeModel", back_populates="schedule_times"
    )
    schedules = relationship(
        "ScheduleModel",
        back_populates="schedule_time",
        cascade="all, delete-orphan",
    )


class ScheduleModel(Base, Timestamps):
    __tablename__ = "schedules"

    id_schendule = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_schendule")

    id_category_subject = Column(
        String(36),
        ForeignKey("category_subjects.id_category_subject", ondelete="CASCADE"),
        nullable=False,
    )
    id_duty_teacher = Column(
        String(36),
        ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True,
    )
    id_class = Column(
        String(36),
        ForeignKey("classes.id_class", ondelete="CASCADE"),
        nullable=False,
    )
    id_schendule_time = Column(
        String(36),
        ForeignKey("schedule_times.id_schendule_time", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(Boolean, default=True, nullable=False)

    category_subject = relationship(
        "CategorySubjectModel", back_populates="schedules"
    )
    duty_teacher = relationship(
        "EmployeeModel", foreign_keys=[id_duty_teacher], back_populates="duty_schedules"
    )
    class_ = relationship("ClassModel", back_populates="schedules")
    schedule_time = relationship("ScheduleTimeModel", back_populates="schedules")
