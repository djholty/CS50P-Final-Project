# Children's Ledger - Web Application

A modern web-based application for managing children's bank accounts, tracking workbook completions, and recording financial transactions. Built with FastAPI, SQLAlchemy, and Bootstrap 5.

## Features

- **Child Account Management**: Create and manage multiple child accounts
- **Transaction Tracking**: Record deposits, withdrawals, and rewards
- **Workbook Completions**: Track completed educational workbooks and tasks
- **Balance Calculation**: Automatic balance calculation with transaction history
- **Beautiful UI**: Modern, responsive interface built with Bootstrap 5
- **Docker Support**: Easy deployment with Docker and docker-compose

## Project Structure

```
CS50P-Final-Project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with routes
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Database CRUD operations
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── child_dashboard.html
│   │   ├── add_child.html
│   │   ├── add_workbook.html
│   │   ├── add_transaction.html
│   │   └── workbooks_list.html
│   └── static/              # Static files (CSS, JS)
│       └── css/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_crud.py         # CRUD operation tests
│   └── test_api.py          # API endpoint tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── PLANNING.md
├── TASK.md
└── README.md
```

## Database Schema

The application uses SQLite with the following tables:

- **Children**: Child accounts (id, name)
- **Workbooks**: Available workbooks/tasks (id, name)
- **Members**: Completed workbooks (children_id, workbooks_id, completed, date)
- **Account**: Financial transactions (id, children_id, date, description, amount)

## Setup Instructions

### Option 1: Docker Deployment (Recommended for Production)

1. **Prerequisites**:
   - Docker installed
   - Docker Compose installed

2. **Build and Run**:
   ```bash
   docker-compose up -d
   ```

3. **Access the Application**:
   - Open your browser to `http://localhost:8000`

4. **Stop the Application**:
   ```bash
   docker-compose down
   ```

5. **View Logs**:
   ```bash
   docker-compose logs -f
   ```

### Option 2: Local Development Setup

1. **Prerequisites**:
   - Python 3.11 or higher
   - pip

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the Application**:
   - Open your browser to `http://localhost:8000`

## Running Tests

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_crud.py

# Run with verbose output
pytest -v
```

## Usage Guide

### Adding a Child

1. Click "Add Child" in the navigation bar
2. Enter the child's name
3. Click "Add Child" button

### Recording a Transaction

1. From the home page, click "Add Transaction" for a specific child
2. Enter the date, description, and amount
   - Positive amounts for deposits/earnings
   - Negative amounts for withdrawals/purchases
3. Click "Add Transaction"

### Recording a Completed Workbook

1. From the home page, click "Complete Workbook" for a specific child
2. Select the date and workbook from the dropdown
3. Click "Record Completion"

### Adding a New Workbook

1. Click "Add Workbook" in the navigation bar
2. Enter the workbook name (e.g., "Grade 3 Math - Addition")
3. Click "Add Workbook"

### Viewing Transaction History

1. Click "View Dashboard" for any child
2. Use the tabs to switch between Transactions and Completed Workbooks
3. Transactions show running balance and cumulative totals

## API Endpoints

### Web Interface Routes

- `GET /` - Home page with all children
- `GET /child/{child_id}` - Child dashboard
- `GET /child/{child_id}/transaction/new` - New transaction form
- `POST /child/{child_id}/transaction` - Create transaction
- `GET /child/{child_id}/workbook/new` - New workbook completion form
- `POST /child/{child_id}/workbook` - Record workbook completion
- `GET /children/new` - New child form
- `POST /children` - Create child
- `GET /workbooks/new` - New workbook form
- `POST /workbooks` - Create workbook
- `GET /workbooks` - List all workbooks

### JSON API Routes

- `GET /api/children` - Get all children with balances (JSON)
- `GET /api/child/{child_id}/transactions` - Get child transactions (JSON)

## Deployment on Local Server

### Using Docker (Recommended)

1. **Install Docker on your local server**:
   - Follow instructions at https://docs.docker.com/engine/install/

2. **Transfer files to server**:
   ```bash
   scp -r . user@server:/path/to/app/
   ```

3. **On the server, build and run**:
   ```bash
   cd /path/to/app
   docker-compose up -d
   ```

4. **Access from local network**:
   - Find server IP: `hostname -I`
   - Access at `http://[SERVER_IP]:8000`

5. **Optional: Set up auto-start on boot**:
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/children-ledger.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Children's Ledger Docker Container
   Requires=docker.service
   After=docker.service

   [Service]
   Type=oneshot
   RemainAfterExit=yes
   WorkingDirectory=/path/to/app
   ExecStart=/usr/bin/docker-compose up -d
   ExecStop=/usr/bin/docker-compose down

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable:
   ```bash
   sudo systemctl enable children-ledger
   sudo systemctl start children-ledger
   ```

## Maintaining Existing Data

The application is designed to work with your existing `ledgerdb.sqlite` database. All historical data is preserved. The CLI script (`project.py`) can still be used as a backup.

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, Jinja2 templates, Bootstrap 5
- **Testing**: Pytest
- **Deployment**: Docker, Docker Compose

## Development

### Code Style

- Follow PEP8 guidelines
- Use type hints
- Write docstrings for all functions (Google style)
- Keep files under 500 lines

### Testing Requirements

For each new feature:
- Write at least 3 tests: success case, edge case, failure case
- Mock external dependencies
- Tests should be in `tests/` directory

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, edit `docker-compose.yml` to change the port mapping:
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

### Database Locked Error

If you get a database locked error, ensure no other processes are accessing the database:
```bash
fuser ledgerdb.sqlite  # Check what's using the file
```

### Permission Errors with Docker

On Linux, if you encounter permission errors:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Contributing

This is a personal project for managing family finances. Contributions are welcome for bug fixes and feature improvements.

## License

Personal use project. Feel free to adapt for your own family needs.

## Acknowledgments

- Built as part of CS50P (CS50's Introduction to Programming with Python)
- Bootstrap for the beautiful UI components
- FastAPI for the excellent web framework

## Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.
