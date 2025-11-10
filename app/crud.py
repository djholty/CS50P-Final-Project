"""
CRUD (Create, Read, Update, Delete) operations.

This module provides database operations for all models,
abstracting the database queries from the API endpoints.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app import models, schemas


# Children CRUD operations

def get_children(db: Session) -> List[models.Child]:
    """
    Get all children from database.
    
    Args:
        db: Database session.
        
    Returns:
        List[models.Child]: List of all children.
    """
    return db.query(models.Child).all()


def get_child(db: Session, child_id: int) -> Optional[models.Child]:
    """
    Get a specific child by ID.
    
    Args:
        db: Database session.
        child_id: Child ID to retrieve.
        
    Returns:
        Optional[models.Child]: Child if found, None otherwise.
    """
    return db.query(models.Child).filter(models.Child.id == child_id).first()


def get_child_by_name(db: Session, name: str) -> Optional[models.Child]:
    """
    Get a child by name.
    
    Args:
        db: Database session.
        name: Child name to search for.
        
    Returns:
        Optional[models.Child]: Child if found, None otherwise.
    """
    return db.query(models.Child).filter(models.Child.name == name).first()


def create_child(db: Session, child: schemas.ChildCreate) -> models.Child:
    """
    Create a new child.
    
    Args:
        db: Database session.
        child: Child data to create.
        
    Returns:
        models.Child: Created child.
    """
    db_child = models.Child(name=child.name)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child


def get_child_balance(db: Session, child_id: int) -> float:
    """
    Calculate current balance for a child.
    
    Args:
        db: Database session.
        child_id: Child ID.
        
    Returns:
        float: Current balance (sum of all transactions).
    """
    result = db.query(func.sum(models.Account.amount)).filter(
        models.Account.children_id == child_id
    ).scalar()
    return result if result is not None else 0.0


# Workbook CRUD operations

def get_workbooks(db: Session) -> List[models.Workbook]:
    """
    Get all workbooks from database.
    
    Args:
        db: Database session.
        
    Returns:
        List[models.Workbook]: List of all workbooks.
    """
    return db.query(models.Workbook).all()


def get_workbook(db: Session, workbook_id: int) -> Optional[models.Workbook]:
    """
    Get a specific workbook by ID.
    
    Args:
        db: Database session.
        workbook_id: Workbook ID to retrieve.
        
    Returns:
        Optional[models.Workbook]: Workbook if found, None otherwise.
    """
    return db.query(models.Workbook).filter(models.Workbook.id == workbook_id).first()


def create_workbook(db: Session, workbook: schemas.WorkbookCreate) -> models.Workbook:
    """
    Create a new workbook.
    
    Args:
        db: Database session.
        workbook: Workbook data to create.
        
    Returns:
        models.Workbook: Created workbook.
    """
    db_workbook = models.Workbook(name=workbook.name)
    db.add(db_workbook)
    db.commit()
    db.refresh(db_workbook)
    return db_workbook


# Transaction CRUD operations

def get_child_transactions(db: Session, child_id: int) -> List[models.Account]:
    """
    Get all transactions for a specific child.
    
    Args:
        db: Database session.
        child_id: Child ID.
        
    Returns:
        List[models.Account]: List of transactions ordered by date.
    """
    return db.query(models.Account).filter(
        models.Account.children_id == child_id
    ).order_by(models.Account.date).all()


def create_transaction(
    db: Session, 
    transaction: schemas.TransactionCreate
) -> models.Account:
    """
    Create a new transaction.
    
    Args:
        db: Database session.
        transaction: Transaction data to create.
        
    Returns:
        models.Account: Created transaction.
    """
    db_transaction = models.Account(
        children_id=transaction.children_id,
        date=transaction.date,
        description=transaction.description,
        amount=transaction.amount
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# Completed Workbook CRUD operations

def get_child_completed_workbooks(db: Session, child_id: int) -> List[dict]:
    """
    Get all completed workbooks for a child with workbook names.
    
    Args:
        db: Database session.
        child_id: Child ID.
        
    Returns:
        List[dict]: List of completed workbooks with details.
    """
    results = db.query(
        models.Member,
        models.Child.name.label('child_name'),
        models.Workbook.name.label('workbook_name')
    ).join(
        models.Child, models.Child.id == models.Member.children_id
    ).join(
        models.Workbook, models.Workbook.id == models.Member.workbooks_id
    ).filter(
        models.Member.children_id == child_id
    ).order_by(models.Member.date).all()
    
    return [
        {
            'children_id': member.children_id,
            'workbooks_id': member.workbooks_id,
            'completed': member.completed,
            'date': member.date,
            'child_name': child_name,
            'workbook_name': workbook_name
        }
        for member, child_name, workbook_name in results
    ]


def create_completed_workbook(
    db: Session,
    completed: schemas.CompletedWorkbookCreate
) -> models.Member:
    """
    Record a completed workbook.
    
    Args:
        db: Database session.
        completed: Completed workbook data.
        
    Returns:
        models.Member: Created completion record.
    """
    db_member = models.Member(
        children_id=completed.children_id,
        workbooks_id=completed.workbooks_id,
        completed=1,
        date=completed.date
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def check_workbook_already_completed(
    db: Session,
    child_id: int,
    workbook_id: int
) -> bool:
    """
    Check if a child has already completed a workbook.
    
    Args:
        db: Database session.
        child_id: Child ID.
        workbook_id: Workbook ID.
        
    Returns:
        bool: True if already completed, False otherwise.
    """
    result = db.query(models.Member).filter(
        models.Member.children_id == child_id,
        models.Member.workbooks_id == workbook_id
    ).first()
    return result is not None


