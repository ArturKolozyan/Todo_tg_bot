from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    remember_time: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"User(id={self.id}"


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'))
    title: Mapped[str] = mapped_column(String())
    body: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}"
