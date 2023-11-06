from sqlalchemy import Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str]
    username: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    image_s3_path: Mapped[str]
    is_blocked: Mapped[bool]
    created_at: Mapped[str]
    modified_at: Mapped[str]

    role: Mapped["Role"] = mapped_column(Enum(Role), nullable=False)

    groups: Mapped["Group"] = relationship("Group", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[str]
