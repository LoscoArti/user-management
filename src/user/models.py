import datetime
import enum
import uuid
from typing import Annotated

from sqlalchemy import Boolean, Enum, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

created_timestamp = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
modified_timestamp = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text)
    surname: Mapped[str] = mapped_column(Text, nullable=True)
    username: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    image_s3_path: Mapped[str] = mapped_column(Text, nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[created_timestamp]
    modified_at: Mapped[modified_timestamp]

    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)

    group: Mapped["Group"] = relationship("Group", back_populates="users")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[created_timestamp]

    users: Mapped[list[User]] = relationship("User", back_populates="group")

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name={self.name})"
