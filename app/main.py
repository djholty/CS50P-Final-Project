"""
FastAPI main application.

This module contains the FastAPI application with all routes
for the children's ledger web interface.
"""

from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import crud, models, schemas
from app.database import engine, get_db, init_db

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Children's Ledger",
    description="Web application for managing children's bank accounts and workbook completions",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Home page showing all children with their current balances.
    
    Args:
        request: FastAPI request object.
        db: Database session.
        
    Returns:
        HTMLResponse: Rendered home page template.
    """
    children = crud.get_children(db)
    children_with_balance = []
    
    for child in children:
        balance = crud.get_child_balance(db, child.id)
        children_with_balance.append({
            'id': child.id,
            'name': child.name,
            'balance': balance
        })
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "children": children_with_balance}
    )


@app.get("/child/{child_id}", response_class=HTMLResponse)
async def child_dashboard(
    request: Request,
    child_id: int,
    db: Session = Depends(get_db)
):
    """
    Child dashboard showing transactions and completed workbooks.
    
    Args:
        request: FastAPI request object.
        child_id: Child ID.
        db: Database session.
        
    Returns:
        HTMLResponse: Rendered child dashboard template.
        
    Raises:
        HTTPException: If child not found.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    transactions = crud.get_child_transactions(db, child_id)
    completed_workbooks = crud.get_child_completed_workbooks(db, child_id)
    balance = crud.get_child_balance(db, child_id)
    
    # Calculate cumulative balance for each transaction
    transactions_with_balance = []
    cumulative = 0.0
    for transaction in transactions:
        cumulative += transaction.amount
        transactions_with_balance.append({
            'id': transaction.id,
            'date': transaction.date,
            'description': transaction.description,
            'amount': transaction.amount,
            'cumulative': cumulative
        })
    
    return templates.TemplateResponse(
        "child_dashboard.html",
        {
            "request": request,
            "child": child,
            "transactions": transactions_with_balance,
            "completed_workbooks": completed_workbooks,
            "balance": balance
        }
    )


@app.get("/child/{child_id}/transaction/new", response_class=HTMLResponse)
async def new_transaction_form(
    request: Request,
    child_id: int,
    db: Session = Depends(get_db)
):
    """
    Form to add a new transaction.
    
    Args:
        request: FastAPI request object.
        child_id: Child ID.
        db: Database session.
        
    Returns:
        HTMLResponse: Rendered transaction form template.
        
    Raises:
        HTTPException: If child not found.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    # Get today's date as default
    today = date.today().strftime("%Y-%m-%d")
    
    return templates.TemplateResponse(
        "add_transaction.html",
        {"request": request, "child": child, "today": today}
    )


@app.post("/child/{child_id}/transaction")
async def create_transaction(
    child_id: int,
    date: str = Form(...),
    description: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction for a child.
    
    Args:
        child_id: Child ID.
        date: Transaction date (YYYY-MM-DD).
        description: Transaction description.
        amount: Transaction amount.
        db: Database session.
        
    Returns:
        RedirectResponse: Redirect to child dashboard.
        
    Raises:
        HTTPException: If child not found or validation fails.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    try:
        transaction_data = schemas.TransactionCreate(
            children_id=child_id,
            date=date,
            description=description,
            amount=amount
        )
        crud.create_transaction(db, transaction_data)
        return RedirectResponse(
            url=f"/child/{child_id}",
            status_code=303
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/child/{child_id}/workbook/new", response_class=HTMLResponse)
async def new_workbook_completion_form(
    request: Request,
    child_id: int,
    db: Session = Depends(get_db)
):
    """
    Form to record a completed workbook.
    
    Args:
        request: FastAPI request object.
        child_id: Child ID.
        db: Database session.
        
    Returns:
        HTMLResponse: Rendered workbook completion form template.
        
    Raises:
        HTTPException: If child not found.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    workbooks = crud.get_workbooks(db)
    today = date.today().strftime("%Y-%m-%d")
    
    return templates.TemplateResponse(
        "add_workbook_completion.html",
        {
            "request": request,
            "child": child,
            "workbooks": workbooks,
            "today": today
        }
    )


@app.post("/child/{child_id}/workbook")
async def create_workbook_completion(
    child_id: int,
    workbook_id: int = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Record a completed workbook for a child.
    
    Args:
        child_id: Child ID.
        workbook_id: Workbook ID.
        date: Completion date (YYYY-MM-DD).
        db: Database session.
        
    Returns:
        RedirectResponse: Redirect to child dashboard.
        
    Raises:
        HTTPException: If child not found, workbook not found, or already completed.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    workbook = crud.get_workbook(db, workbook_id)
    if not workbook:
        raise HTTPException(status_code=404, detail="Workbook not found")
    
    # Check if already completed
    if crud.check_workbook_already_completed(db, child_id, workbook_id):
        raise HTTPException(
            status_code=400,
            detail="This workbook has already been completed by this child"
        )
    
    try:
        completion_data = schemas.CompletedWorkbookCreate(
            children_id=child_id,
            workbooks_id=workbook_id,
            date=date
        )
        crud.create_completed_workbook(db, completion_data)
        return RedirectResponse(
            url=f"/child/{child_id}",
            status_code=303
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/children/new", response_class=HTMLResponse)
async def new_child_form(request: Request):
    """
    Form to add a new child.
    
    Args:
        request: FastAPI request object.
        
    Returns:
        HTMLResponse: Rendered child form template.
    """
    return templates.TemplateResponse(
        "add_child.html",
        {"request": request}
    )


@app.post("/children")
async def create_child(
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Create a new child.
    
    Args:
        name: Child name.
        db: Database session.
        
    Returns:
        RedirectResponse: Redirect to home page.
        
    Raises:
        HTTPException: If child name already exists.
    """
    # Check if child already exists
    existing_child = crud.get_child_by_name(db, name)
    if existing_child:
        raise HTTPException(
            status_code=400,
            detail="A child with this name already exists"
        )
    
    try:
        child_data = schemas.ChildCreate(name=name)
        crud.create_child(db, child_data)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/workbooks/new", response_class=HTMLResponse)
async def new_workbook_form(request: Request):
    """
    Form to add a new workbook.
    
    Args:
        request: FastAPI request object.
        
    Returns:
        HTMLResponse: Rendered workbook form template.
    """
    return templates.TemplateResponse(
        "add_workbook.html",
        {"request": request}
    )


@app.post("/workbooks")
async def create_workbook(
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Create a new workbook.
    
    Args:
        name: Workbook name.
        db: Database session.
        
    Returns:
        RedirectResponse: Redirect to home page.
        
    Raises:
        HTTPException: If validation fails.
    """
    try:
        workbook_data = schemas.WorkbookCreate(name=name)
        crud.create_workbook(db, workbook_data)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/workbooks", response_class=HTMLResponse)
async def list_workbooks(request: Request, db: Session = Depends(get_db)):
    """
    List all workbooks.
    
    Args:
        request: FastAPI request object.
        db: Database session.
        
    Returns:
        HTMLResponse: Rendered workbooks list template.
    """
    workbooks = crud.get_workbooks(db)
    return templates.TemplateResponse(
        "workbooks_list.html",
        {"request": request, "workbooks": workbooks}
    )


# API endpoints for JSON responses

@app.get("/api/children", response_model=List[schemas.ChildResponse])
async def api_get_children(db: Session = Depends(get_db)):
    """
    API endpoint to get all children with balances.
    
    Args:
        db: Database session.
        
    Returns:
        List[schemas.ChildResponse]: List of children with balances.
    """
    children = crud.get_children(db)
    response = []
    for child in children:
        balance = crud.get_child_balance(db, child.id)
        response.append(
            schemas.ChildResponse(
                id=child.id,
                name=child.name,
                balance=balance
            )
        )
    return response


@app.get("/api/child/{child_id}/transactions", response_model=List[schemas.TransactionResponse])
async def api_get_transactions(child_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get all transactions for a child.
    
    Args:
        child_id: Child ID.
        db: Database session.
        
    Returns:
        List[schemas.TransactionResponse]: List of transactions.
        
    Raises:
        HTTPException: If child not found.
    """
    child = crud.get_child(db, child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    return crud.get_child_transactions(db, child_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


