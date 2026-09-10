"""SQLite configuration and request-scoped SQLAlchemy sessions."""

from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tri9t.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for application models."""


def get_db() -> Generator[Session, None, None]:
    """Yield and safely close one database session per request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
