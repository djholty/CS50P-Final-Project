"""
SQLAlchemy ORM models.

Defines database models matching the existing schema:
- Children: Child accounts
- Workbooks: Available workbook tasks
- Members: Many-to-many relationship for completed workbooks
- Account: Financial transactions
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Child(Base):
    """
    Represents a child with an account.
    
    Attributes:
        id: Primary key
        name: Unique child name
        account_entries: Relationship to Account transactions
        completed_workbooks: Relationship to completed workbooks
    """
    __tablename__ = "Children"
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(Text, unique=True)
    
    # Relationships
    account_entries = relationship("Account", back_populates="child")
    completed_workbooks = relationship("Member", back_populates="child")


class Workbook(Base):
    """
    Represents a workbook/task that can be completed.
    
    Attributes:
        id: Primary key
        name: Workbook title/name
        completions: Relationship to Member records
    """
    __tablename__ = "Workbooks"
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    name = Column(Text)
    
    # Relationships
    completions = relationship("Member", back_populates="workbook")


class Member(Base):
    """
    Represents a completed workbook by a child.
    
    Many-to-many relationship between Children and Workbooks.
    
    Attributes:
        children_id: Foreign key to Children
        workbooks_id: Foreign key to Workbooks
        completed: Completion status (1 = completed)
        date: Date of completion (YYYY-MM-DD format)
    """
    __tablename__ = "Members"
    
    children_id = Column(Integer, ForeignKey('Children.id'), primary_key=True)
    workbooks_id = Column(Integer, ForeignKey('Workbooks.id'), primary_key=True)
    completed = Column(Integer)
    date = Column(Text)
    
    # Relationships
    child = relationship("Child", back_populates="completed_workbooks")
    workbook = relationship("Workbook", back_populates="completions")


class Account(Base):
    """
    Represents a financial transaction for a child.
    
    Attributes:
        id: Primary key
        children_id: Foreign key to Children
        date: Transaction date (YYYY-MM-DD format)
        description: Transaction description (max 60 chars)
        amount: Transaction amount (positive = credit, negative = debit)
    """
    __tablename__ = "Account"
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    children_id = Column(Integer, ForeignKey('Children.id'))
    date = Column(Text)
    description = Column(Text)
    amount = Column(Float)
    
    # Relationships
    child = relationship("Child", back_populates="account_entries")


