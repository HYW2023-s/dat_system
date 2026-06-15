"""SQLAlchemy ORM models."""

from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, SmallInteger, Boolean, Text,
)
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import Base


class User(Base):
    """User model for authentication."""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)


class DatTest(Base):
    """DAT test records."""
    __tablename__ = "dat_test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), default="", index=True)
    create_time = Column(DateTime, default=datetime.now)
    word1 = Column(String(32), default="")
    word2 = Column(String(32), default="")
    word3 = Column(String(32), default="")
    word4 = Column(String(32), default="")
    word5 = Column(String(32), default="")
    word6 = Column(String(32), default="")
    word7 = Column(String(32), default="")
    word8 = Column(String(32), default="")
    word9 = Column(String(32), default="")
    word10 = Column(String(32), default="")
    dat_score = Column(Integer, default=0)
    effective_num = Column(Integer, default=0)
    picture_path = Column(String(256), nullable=True)
    spend_time = Column(String(32), default="")
    limited_time = Column(String(32), default="")


class AnswerLog(Base):
    """Answer log - records when users start/finish a test."""
    __tablename__ = "answer_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), default="")
    create_time = Column(DateTime, default=datetime.now)
    statue = Column(SmallInteger, default=0)  # 0: start, 1: finish


class SpendTime(Base):
    """Records time spent on tests."""
    __tablename__ = "spend_time"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), default="")
    create_time = Column(DateTime, default=datetime.now)
    spend_time = Column(String(32))


class TaskTime(Base):
    """Task configuration - time limits etc."""
    __tablename__ = "task_time"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(32), default="DAT")
    limited_time = Column(Integer, default=240)  # seconds


async def ensure_default_admin(session: AsyncSession):
    """Create default admin user if not exists."""
    from sqlalchemy import select
    from passlib.hash import bcrypt
    from backend.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

    result = await session.execute(
        select(User).where(User.username == DEFAULT_ADMIN_USERNAME)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            username=DEFAULT_ADMIN_USERNAME,
            password_hash=bcrypt.hash(DEFAULT_ADMIN_PASSWORD),
            is_superuser=True,
        )
        session.add(user)
        await session.commit()


async def ensure_default_task_time(session: AsyncSession):
    """Create default task time config if not exists."""
    from sqlalchemy import select
    from backend.config import DEFAULT_LIMITED_TIME

    result = await session.execute(
        select(TaskTime).where(TaskTime.task_name == "DAT")
    )
    task_time = result.scalar_one_or_none()

    if task_time is None:
        task_time = TaskTime(task_name="DAT", limited_time=DEFAULT_LIMITED_TIME)
        session.add(task_time)
        await session.commit()
