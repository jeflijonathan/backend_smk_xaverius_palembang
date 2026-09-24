import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class ClassRoomModel(Base, Timestamps):
    __tablename__ = "classrooms"

    id_class_room = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_class_room")

    id_teacher_subject = Column(
        String(36),
        ForeignKey("teacher_subjects.id_teacher_subject", ondelete="CASCADE"),
        nullable=False,
    )
    id_class = Column(
        String(36),
        ForeignKey("classes.id_class", ondelete="CASCADE"),
        nullable=False,
    )
    id_school_information = Column(
        String(36),
        ForeignKey("school_informations.id_school_information", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(Boolean, default=True, nullable=False)

    teacher_subject = relationship(
        "TeacherSubjectModel", back_populates="classrooms"
    )
    class_ = relationship("ClassModel", back_populates="classrooms")
    school_information = relationship(
        "SchoolInformationModel", back_populates="classrooms"
    )
