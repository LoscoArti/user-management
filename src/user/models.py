import datetime
import enum
from typing import Annotated

from sqlalchemy import Enum, ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
modified_at = Annotated[
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

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(Text(30), nullable=False)
    surname: Mapped[str]
    username: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    image_s3_path: Mapped[str]
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at] = mapped_column(default=created_at)
    modified_at: Mapped[modified_at]

    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.USER)

    group_id: Mapped[int] = relationship(ForeignKey("groups.id"))

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(Text(50), nullable=False)
    created_at: Mapped[created_at] = mapped_column(default=created_at)
