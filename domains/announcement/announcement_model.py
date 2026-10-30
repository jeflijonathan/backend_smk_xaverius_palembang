import uuid
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class AnnouncementUserLogModel(Base, Timestamps):
    __tablename__ = "announcement_user_logs"
    
    id_log = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    id_announcement = Column(String(36), ForeignKey("announcement.id_announcement", ondelete="CASCADE"), nullable=False)
    id_user = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False) # e.g. "created", "updated"
    
    # Relationships
    announcement = relationship("AnnouncementModel", back_populates="user_logs")
    user = relationship("UserModel")


class AnnouncementModel(Base, Timestamps):
    __tablename__ = "announcement"

    id_announcement = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url_drive = Column(String(255), nullable=True)

    user_logs = relationship("AnnouncementUserLogModel", back_populates="announcement", cascade="all, delete-orphan")
