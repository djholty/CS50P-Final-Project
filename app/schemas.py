"""
Pydantic schemas for request/response validation.

These schemas define the structure of data for API requests and responses,
providing automatic validation and serialization.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date


class ChildBase(BaseModel):
    """Base schema for Child."""
    name: str = Field(..., min_length=1, max_length=100)


class ChildCreate(ChildBase):
    """Schema for creating a new child."""
    pass


class ChildResponse(ChildBase):
    """Schema for child response with ID and balance."""
    id: int
    balance: Optional[float] = 0.0
    
    class Config:
        from_attributes = True


class WorkbookBase(BaseModel):
    """Base schema for Workbook."""
    name: str = Field(..., min_length=1, max_length=200)


class WorkbookCreate(WorkbookBase):
    """Schema for creating a new workbook."""
    pass


class WorkbookResponse(WorkbookBase):
    """Schema for workbook response."""
    id: int
    
    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    """Base schema for Account transaction."""
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    description: str = Field(..., min_length=1, max_length=60)
    amount: float
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        """
        Validate date format is YYYY-MM-DD.
        
        Args:
            v: Date string to validate.
            
        Returns:
            str: Validated date string.
            
        Raises:
            ValueError: If date format is invalid.
        """
        try:
            year, month, day = v.split('-')
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            
            if len(year) != 4 or len(month) != 2 or len(day) != 2:
                raise ValueError("Date must be in YYYY-MM-DD format")
            
            if month_int < 1 or month_int > 12:
                raise ValueError("Month must be between 01 and 12")
            
            if day_int < 1 or day_int > 31:
                raise ValueError("Day must be between 01 and 31")
            
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    children_id: int


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    children_id: int
    
    class Config:
        from_attributes = True


class CompletedWorkbookBase(BaseModel):
    """Base schema for completed workbook."""
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        """
        Validate date format is YYYY-MM-DD.
        
        Args:
            v: Date string to validate.
            
        Returns:
            str: Validated date string.
            
        Raises:
            ValueError: If date format is invalid.
        """
        try:
            year, month, day = v.split('-')
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            
            if len(year) != 4 or len(month) != 2 or len(day) != 2:
                raise ValueError("Date must be in YYYY-MM-DD format")
            
            if month_int < 1 or month_int > 12:
                raise ValueError("Month must be between 01 and 12")
            
            if day_int < 1 or day_int > 31:
                raise ValueError("Day must be between 01 and 31")
            
            return v
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")


class CompletedWorkbookCreate(CompletedWorkbookBase):
    """Schema for recording a completed workbook."""
    children_id: int
    workbooks_id: int


class CompletedWorkbookResponse(CompletedWorkbookBase):
    """Schema for completed workbook response."""
    children_id: int
    workbooks_id: int
    completed: int
    child_name: Optional[str] = None
    workbook_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChildDashboard(BaseModel):
    """Schema for child dashboard data."""
    child: ChildResponse
    transactions: List[TransactionResponse]
    completed_workbooks: List[CompletedWorkbookResponse]
    balance: float


