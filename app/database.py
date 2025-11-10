"""
Database configuration and session management.

This module handles SQLite database connections and provides
session management for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Database URL - using the existing ledgerdb.sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./ledgerdb.sqlite"

# Create engine with connect_args for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session.
    
    Example:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(models.Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    
    Creates all tables defined in models if they don't exist.
    Does not drop existing tables.
    """
    Base.metadata.create_all(bind=engine)


