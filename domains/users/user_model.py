import uuid
from sqlalchemy import Column, String, ForeignKey, Table, Text, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


from domains.auth.role_model import RoleModel
from domains.auth.associations import user_roles_association


class UserModel(Base, Timestamps):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    roles = relationship(
        "RoleModel", secondary=user_roles_association, back_populates="users"
    )

