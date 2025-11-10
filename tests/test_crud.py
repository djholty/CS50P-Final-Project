"""
Unit tests for CRUD operations.

Tests all database operations defined in app/crud.py.
"""

import pytest
from app import crud, schemas, models


class TestChildCRUD:
    """Tests for child CRUD operations."""
    
    def test_create_child_success(self, test_db):
        """Test creating a child successfully."""
        child_data = schemas.ChildCreate(name="Alice")
        child = crud.create_child(test_db, child_data)
        
        assert child.id is not None
        assert child.name == "Alice"
    
    def test_get_children(self, test_db, sample_child):
        """Test retrieving all children."""
        children = crud.get_children(test_db)
        
        assert len(children) >= 1
        assert any(c.name == sample_child.name for c in children)
    
    def test_get_child_by_id(self, test_db, sample_child):
        """Test retrieving a child by ID."""
        child = crud.get_child(test_db, sample_child.id)
        
        assert child is not None
        assert child.id == sample_child.id
        assert child.name == sample_child.name
    
    def test_get_child_not_found(self, test_db):
        """Test retrieving a non-existent child."""
        child = crud.get_child(test_db, 99999)
        
        assert child is None
    
    def test_get_child_by_name(self, test_db, sample_child):
        """Test retrieving a child by name."""
        child = crud.get_child_by_name(test_db, sample_child.name)
        
        assert child is not None
        assert child.name == sample_child.name
    
    def test_get_child_balance_zero(self, test_db, sample_child):
        """Test getting balance for child with no transactions."""
        balance = crud.get_child_balance(test_db, sample_child.id)
        
        assert balance == 0.0
    
    def test_get_child_balance_with_transactions(self, test_db, sample_child):
        """Test getting balance for child with transactions."""
        # Add transactions
        transaction1 = models.Account(
            children_id=sample_child.id,
            date="2025-01-01",
            description="Earned money",
            amount=50.00
        )
        transaction2 = models.Account(
            children_id=sample_child.id,
            date="2025-01-02",
            description="Spent money",
            amount=-20.00
        )
        test_db.add(transaction1)
        test_db.add(transaction2)
        test_db.commit()
        
        balance = crud.get_child_balance(test_db, sample_child.id)
        
        assert balance == 30.00


class TestWorkbookCRUD:
    """Tests for workbook CRUD operations."""
    
    def test_create_workbook_success(self, test_db):
        """Test creating a workbook successfully."""
        workbook_data = schemas.WorkbookCreate(name="Grade 2 Reading")
        workbook = crud.create_workbook(test_db, workbook_data)
        
        assert workbook.id is not None
        assert workbook.name == "Grade 2 Reading"
    
    def test_get_workbooks(self, test_db, sample_workbook):
        """Test retrieving all workbooks."""
        workbooks = crud.get_workbooks(test_db)
        
        assert len(workbooks) >= 1
        assert any(w.name == sample_workbook.name for w in workbooks)
    
    def test_get_workbook_by_id(self, test_db, sample_workbook):
        """Test retrieving a workbook by ID."""
        workbook = crud.get_workbook(test_db, sample_workbook.id)
        
        assert workbook is not None
        assert workbook.id == sample_workbook.id
        assert workbook.name == sample_workbook.name
    
    def test_get_workbook_not_found(self, test_db):
        """Test retrieving a non-existent workbook."""
        workbook = crud.get_workbook(test_db, 99999)
        
        assert workbook is None


class TestTransactionCRUD:
    """Tests for transaction CRUD operations."""
    
    def test_create_transaction_success(self, test_db, sample_child):
        """Test creating a transaction successfully."""
        transaction_data = schemas.TransactionCreate(
            children_id=sample_child.id,
            date="2025-01-15",
            description="Allowance",
            amount=10.00
        )
        transaction = crud.create_transaction(test_db, transaction_data)
        
        assert transaction.id is not None
        assert transaction.children_id == sample_child.id
        assert transaction.description == "Allowance"
        assert transaction.amount == 10.00
    
    def test_create_transaction_negative_amount(self, test_db, sample_child):
        """Test creating a transaction with negative amount (withdrawal)."""
        transaction_data = schemas.TransactionCreate(
            children_id=sample_child.id,
            date="2025-01-15",
            description="Toy purchase",
            amount=-15.50
        )
        transaction = crud.create_transaction(test_db, transaction_data)
        
        assert transaction.amount == -15.50
    
    def test_get_child_transactions(self, test_db, sample_child, sample_transaction):
        """Test retrieving all transactions for a child."""
        transactions = crud.get_child_transactions(test_db, sample_child.id)
        
        assert len(transactions) >= 1
        assert any(t.id == sample_transaction.id for t in transactions)
    
    def test_get_child_transactions_ordered_by_date(self, test_db, sample_child):
        """Test that transactions are ordered by date."""
        # Add transactions in non-chronological order
        t1 = models.Account(
            children_id=sample_child.id,
            date="2025-01-15",
            description="Transaction 2",
            amount=10.00
        )
        t2 = models.Account(
            children_id=sample_child.id,
            date="2025-01-10",
            description="Transaction 1",
            amount=5.00
        )
        test_db.add(t1)
        test_db.add(t2)
        test_db.commit()
        
        transactions = crud.get_child_transactions(test_db, sample_child.id)
        
        # First transaction should be the earlier date
        assert transactions[0].date == "2025-01-10"
        assert transactions[1].date == "2025-01-15"


class TestCompletedWorkbookCRUD:
    """Tests for completed workbook CRUD operations."""
    
    def test_create_completed_workbook_success(self, test_db, sample_child, sample_workbook):
        """Test recording a completed workbook successfully."""
        completion_data = schemas.CompletedWorkbookCreate(
            children_id=sample_child.id,
            workbooks_id=sample_workbook.id,
            date="2025-01-20"
        )
        completion = crud.create_completed_workbook(test_db, completion_data)
        
        assert completion.children_id == sample_child.id
        assert completion.workbooks_id == sample_workbook.id
        assert completion.completed == 1
        assert completion.date == "2025-01-20"
    
    def test_check_workbook_already_completed(self, test_db, sample_child, sample_workbook):
        """Test checking if workbook is already completed."""
        # Initially not completed
        assert not crud.check_workbook_already_completed(
            test_db, sample_child.id, sample_workbook.id
        )
        
        # Add completion
        completion_data = schemas.CompletedWorkbookCreate(
            children_id=sample_child.id,
            workbooks_id=sample_workbook.id,
            date="2025-01-20"
        )
        crud.create_completed_workbook(test_db, completion_data)
        
        # Now it should be completed
        assert crud.check_workbook_already_completed(
            test_db, sample_child.id, sample_workbook.id
        )
    
    def test_get_child_completed_workbooks(self, test_db, sample_child, sample_workbook):
        """Test retrieving completed workbooks for a child."""
        # Add completion
        completion_data = schemas.CompletedWorkbookCreate(
            children_id=sample_child.id,
            workbooks_id=sample_workbook.id,
            date="2025-01-20"
        )
        crud.create_completed_workbook(test_db, completion_data)
        
        # Retrieve completions
        completions = crud.get_child_completed_workbooks(test_db, sample_child.id)
        
        assert len(completions) >= 1
        assert completions[0]['children_id'] == sample_child.id
        assert completions[0]['workbooks_id'] == sample_workbook.id
        assert completions[0]['workbook_name'] == sample_workbook.name
    
    def test_get_child_completed_workbooks_empty(self, test_db, sample_child):
        """Test retrieving completed workbooks when none exist."""
        completions = crud.get_child_completed_workbooks(test_db, sample_child.id)
        
        assert len(completions) == 0


