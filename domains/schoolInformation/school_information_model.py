import uuid
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class SchoolInformationModel(Base, Timestamps):
    __tablename__ = "school_informations"

    id_school_information = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    id = synonym("id_school_information")

    name_school = Column(String(255), nullable=False)
    periode = Column(String(100), nullable=True)
    NPSN = Column(String(50), nullable=True)
    id_headmaster = Column(String(36), ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    alamat = Column(Text, nullable=True)
    status = Column(Boolean, default=True, nullable=False)

    headmaster = relationship(
        "EmployeeModel",
        foreign_keys=[id_headmaster],
        back_populates="headmaster_schools"
    )
    classrooms = relationship(
        "ClassRoomModel",
        back_populates="school_information",
        cascade="all, delete-orphan"
    )
