"""
Pytest configuration and fixtures.

This module provides shared fixtures for testing the application.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app import models


# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_ledger.sqlite"


@pytest.fixture(scope="function")
def test_engine():
    """
    Create a test database engine.
    
    Yields:
        Engine: SQLAlchemy engine for testing.
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """
    Create a test database session.
    
    Args:
        test_engine: Test database engine fixture.
        
    Yields:
        Session: Database session for testing.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a test client with database override.
    
    Args:
        test_db: Test database session fixture.
        
    Yields:
        TestClient: FastAPI test client.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_child(test_db):
    """
    Create a sample child for testing.
    
    Args:
        test_db: Test database session fixture.
        
    Returns:
        models.Child: Created child instance.
    """
    child = models.Child(name="Test Child")
    test_db.add(child)
    test_db.commit()
    test_db.refresh(child)
    return child


@pytest.fixture(scope="function")
def sample_workbook(test_db):
    """
    Create a sample workbook for testing.
    
    Args:
        test_db: Test database session fixture.
        
    Returns:
        models.Workbook: Created workbook instance.
    """
    workbook = models.Workbook(name="Test Workbook - Grade 1 Math")
    test_db.add(workbook)
    test_db.commit()
    test_db.refresh(workbook)
    return workbook


@pytest.fixture(scope="function")
def sample_transaction(test_db, sample_child):
    """
    Create a sample transaction for testing.
    
    Args:
        test_db: Test database session fixture.
        sample_child: Sample child fixture.
        
    Returns:
        models.Account: Created transaction instance.
    """
    transaction = models.Account(
        children_id=sample_child.id,
        date="2025-01-01",
        description="Test Transaction",
        amount=25.00
    )
    test_db.add(transaction)
    test_db.commit()
    test_db.refresh(transaction)
    return transaction


