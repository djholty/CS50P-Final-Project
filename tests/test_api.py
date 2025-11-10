"""
Unit tests for API endpoints.

Tests all API routes defined in app/main.py.
"""

import pytest
from fastapi.testclient import TestClient


class TestHomeEndpoint:
    """Tests for home page endpoint."""
    
    def test_home_page_loads(self, client):
        """Test that home page loads successfully."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert b"Children's Bank Accounts" in response.content
    
    def test_home_page_shows_children(self, client, sample_child):
        """Test that home page displays children."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert sample_child.name.encode() in response.content


class TestChildEndpoints:
    """Tests for child-related endpoints."""
    
    def test_create_child_success(self, client):
        """Test creating a child via API."""
        response = client.post(
            "/children",
            data={"name": "Bob"}
        )
        
        assert response.status_code == 303  # Redirect
        assert response.headers["location"] == "/"
    
    def test_create_child_duplicate_name(self, client, sample_child):
        """Test that duplicate child names are rejected."""
        response = client.post(
            "/children",
            data={"name": sample_child.name}
        )
        
        assert response.status_code == 400
    
    def test_get_child_dashboard(self, client, sample_child):
        """Test accessing a child's dashboard."""
        response = client.get(f"/child/{sample_child.id}")
        
        assert response.status_code == 200
        assert sample_child.name.encode() in response.content
        assert b"Current Balance" in response.content
    
    def test_get_child_dashboard_not_found(self, client):
        """Test accessing dashboard for non-existent child."""
        response = client.get("/child/99999")
        
        assert response.status_code == 404
    
    def test_new_child_form(self, client):
        """Test that new child form loads."""
        response = client.get("/children/new")
        
        assert response.status_code == 200
        assert b"Add New Child" in response.content


class TestWorkbookEndpoints:
    """Tests for workbook-related endpoints."""
    
    def test_create_workbook_success(self, client):
        """Test creating a workbook via API."""
        response = client.post(
            "/workbooks",
            data={"name": "Grade 3 Science"}
        )
        
        assert response.status_code == 303  # Redirect
        assert response.headers["location"] == "/"
    
    def test_list_workbooks(self, client, sample_workbook):
        """Test listing all workbooks."""
        response = client.get("/workbooks")
        
        assert response.status_code == 200
        assert sample_workbook.name.encode() in response.content
    
    def test_new_workbook_form(self, client):
        """Test that new workbook form loads."""
        response = client.get("/workbooks/new")
        
        assert response.status_code == 200
        assert b"Add New Workbook" in response.content


class TestTransactionEndpoints:
    """Tests for transaction-related endpoints."""
    
    def test_create_transaction_success(self, client, sample_child):
        """Test creating a transaction via API."""
        response = client.post(
            f"/child/{sample_child.id}/transaction",
            data={
                "date": "2025-01-25",
                "description": "Chores completed",
                "amount": "15.00"
            }
        )
        
        assert response.status_code == 303  # Redirect
        assert response.headers["location"] == f"/child/{sample_child.id}"
    
    def test_create_transaction_negative_amount(self, client, sample_child):
        """Test creating a withdrawal transaction."""
        response = client.post(
            f"/child/{sample_child.id}/transaction",
            data={
                "date": "2025-01-25",
                "description": "Toy purchase",
                "amount": "-12.50"
            }
        )
        
        assert response.status_code == 303  # Redirect
    
    def test_create_transaction_invalid_date(self, client, sample_child):
        """Test that invalid date format is rejected."""
        response = client.post(
            f"/child/{sample_child.id}/transaction",
            data={
                "date": "invalid-date",
                "description": "Test",
                "amount": "10.00"
            }
        )
        
        assert response.status_code == 400
    
    def test_create_transaction_child_not_found(self, client):
        """Test creating transaction for non-existent child."""
        response = client.post(
            "/child/99999/transaction",
            data={
                "date": "2025-01-25",
                "description": "Test",
                "amount": "10.00"
            }
        )
        
        assert response.status_code == 404
    
    def test_new_transaction_form(self, client, sample_child):
        """Test that new transaction form loads."""
        response = client.get(f"/child/{sample_child.id}/transaction/new")
        
        assert response.status_code == 200
        assert b"Add Transaction" in response.content


class TestWorkbookCompletionEndpoints:
    """Tests for workbook completion endpoints."""
    
    def test_create_workbook_completion_success(self, client, sample_child, sample_workbook):
        """Test recording a completed workbook via API."""
        response = client.post(
            f"/child/{sample_child.id}/workbook",
            data={
                "workbook_id": str(sample_workbook.id),
                "date": "2025-01-25"
            }
        )
        
        assert response.status_code == 303  # Redirect
        assert response.headers["location"] == f"/child/{sample_child.id}"
    
    def test_create_workbook_completion_duplicate(self, client, sample_child, sample_workbook):
        """Test that duplicate completions are rejected."""
        # First completion
        client.post(
            f"/child/{sample_child.id}/workbook",
            data={
                "workbook_id": str(sample_workbook.id),
                "date": "2025-01-25"
            }
        )
        
        # Attempt duplicate
        response = client.post(
            f"/child/{sample_child.id}/workbook",
            data={
                "workbook_id": str(sample_workbook.id),
                "date": "2025-01-26"
            }
        )
        
        assert response.status_code == 400
    
    def test_create_workbook_completion_invalid_workbook(self, client, sample_child):
        """Test recording completion for non-existent workbook."""
        response = client.post(
            f"/child/{sample_child.id}/workbook",
            data={
                "workbook_id": "99999",
                "date": "2025-01-25"
            }
        )
        
        assert response.status_code == 404
    
    def test_new_workbook_completion_form(self, client, sample_child):
        """Test that workbook completion form loads."""
        response = client.get(f"/child/{sample_child.id}/workbook/new")
        
        assert response.status_code == 200
        assert b"Record Completed Workbook" in response.content


class TestAPIEndpoints:
    """Tests for JSON API endpoints."""
    
    def test_api_get_children(self, client, sample_child):
        """Test API endpoint for getting all children."""
        response = client.get("/api/children")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(child["name"] == sample_child.name for child in data)
    
    def test_api_get_transactions(self, client, sample_child, sample_transaction):
        """Test API endpoint for getting child transactions."""
        response = client.get(f"/api/child/{sample_child.id}/transactions")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(t["id"] == sample_transaction.id for t in data)
    
    def test_api_get_transactions_child_not_found(self, client):
        """Test API transactions endpoint for non-existent child."""
        response = client.get("/api/child/99999/transactions")
        
        assert response.status_code == 404


