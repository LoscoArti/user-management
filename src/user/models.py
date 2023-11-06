from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class RoleEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    group_id = Column(Integer, ForeignKey("groups.id"))
    image_s3_path = Column(String)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    group = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime)

    users = relationship("User", back_populates="group")
