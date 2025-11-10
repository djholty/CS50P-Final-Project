# Children's Ledger - Project Planning

## Project Overview

This document outlines the architecture, design decisions, and technical specifications for the Children's Ledger web application.

## Goals

1. Transform CLI-based ledger into modern web application
2. Preserve all existing data and functionality
3. Provide intuitive, child-friendly interface
4. Enable easy deployment on local server
5. Maintain code quality with comprehensive tests

## Architecture

### Technology Stack

**Backend**:
- FastAPI: Modern, fast Python web framework with automatic API documentation
- SQLAlchemy: ORM for database operations
- Pydantic: Data validation and serialization
- Uvicorn: ASGI server for running the application

**Frontend**:
- Jinja2: Server-side templating
- Bootstrap 5: Responsive UI framework
- Vanilla JavaScript: Minimal client-side interactions

**Database**:
- SQLite: Lightweight, file-based database (existing ledgerdb.sqlite)

**Deployment**:
- Docker: Containerization for consistent deployment
- Docker Compose: Multi-container orchestration

**Testing**:
- Pytest: Unit and integration testing
- TestClient: FastAPI testing utilities

### Design Patterns

1. **Repository Pattern**: CRUD operations abstracted in `crud.py`
2. **Dependency Injection**: Database sessions provided via FastAPI dependencies
3. **MVC Pattern**: Models (SQLAlchemy), Views (Jinja2 templates), Controllers (FastAPI routes)
4. **Schema Validation**: Pydantic models for request/response validation

## Database Schema

### Existing Schema (Preserved)

The application works with the existing database schema:

```sql
-- Children table
CREATE TABLE Children (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name TEXT UNIQUE
);

-- Workbooks table
CREATE TABLE Workbooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name TEXT
);

-- Members table (many-to-many: children <-> workbooks)
CREATE TABLE Members (
    children_id INTEGER,
    workbooks_id INTEGER,
    completed INTEGER,
    date TEXT,
    PRIMARY KEY (children_id, workbooks_id),
    FOREIGN KEY (children_id) REFERENCES Children(id),
    FOREIGN KEY (workbooks_id) REFERENCES Workbooks(id)
);

-- Account table (transactions)
CREATE TABLE Account (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    children_id INTEGER,
    date TEXT,
    description TEXT,
    amount REAL,
    FOREIGN KEY (children_id) REFERENCES Children(id)
);
```

### Design Decisions

1. **Date Format**: YYYY-MM-DD string format (ISO 8601)
   - Reason: Simple, sortable, human-readable
   - Validated in Pydantic schemas

2. **Amount Type**: REAL (floating-point)
   - Positive: Deposits, earnings
   - Negative: Withdrawals, purchases

3. **Composite Primary Key**: (children_id, workbooks_id) in Members
   - Reason: Prevents duplicate completions
   - Each child can complete each workbook once

## Application Structure

### Module Organization

```
app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI app, routes, endpoints
├── database.py          # DB connection, session management
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic validation schemas
├── crud.py              # Database CRUD operations
├── templates/           # HTML templates
└── static/              # Static assets
```

### Key Components

#### 1. Database Layer (`database.py`)

- Connection management
- Session factory
- Dependency function for route injection

#### 2. Models Layer (`models.py`)

- ORM models matching database schema
- Relationships defined
- Type annotations

#### 3. Schemas Layer (`schemas.py`)

- Request/response validation
- Data serialization
- Custom validators for dates

#### 4. CRUD Layer (`crud.py`)

- Abstracted database operations
- Business logic for data access
- Separation from routes

#### 5. Routes Layer (`main.py`)

- HTTP endpoints
- Form handling
- Template rendering
- JSON API endpoints

## API Design

### Web Interface (HTML)

Following RESTful principles where applicable:

- `GET /` → List all children
- `GET /child/{id}` → View child dashboard
- `POST /child/{id}/transaction` → Create transaction
- `POST /child/{id}/workbook` → Record completion
- `GET /children/new` → Form
- `POST /children` → Create child

### JSON API

Separate endpoints for programmatic access:

- `GET /api/children` → JSON list of children
- `GET /api/child/{id}/transactions` → JSON transactions

## UI/UX Design

### Design Principles

1. **Simplicity**: Clean, uncluttered interface
2. **Child-Friendly**: Large buttons, clear icons
3. **Responsive**: Works on phones, tablets, desktops
4. **Feedback**: Clear success/error messages
5. **Navigation**: Breadcrumbs, back buttons

### Color Scheme

- Primary: Blue (#4a90e2) - Trust, stability
- Success: Green (#5cb85c) - Positive actions
- Danger: Red (#d9534f) - Negative actions
- Neutral: Gray tones

### Visual Indicators

- Credit transactions: Green background
- Debit transactions: Red background
- Current balance: Large, prominent display
- Icons: Bootstrap Icons for consistency

## Testing Strategy

### Test Coverage

1. **Unit Tests** (`test_crud.py`):
   - Each CRUD function
   - Edge cases (empty, invalid input)
   - Database constraints

2. **Integration Tests** (`test_api.py`):
   - API endpoints
   - Form submissions
   - Authentication flows (if added)

3. **Test Database**:
   - Separate SQLite file
   - Fresh for each test
   - Isolated from production

### Testing Approach

- **Fixtures**: Reusable test data (conftest.py)
- **Mocking**: Database mocked where appropriate
- **Coverage**: Aim for >80% code coverage
- **CI/CD**: Tests run before deployment

## Security Considerations

### Current Implementation

- No authentication (family use on local network)
- Input validation via Pydantic
- SQL injection prevention via SQLAlchemy
- No exposed ports externally

### Future Enhancements

If exposing to internet:
1. Add authentication (FastAPI security)
2. HTTPS/TLS encryption
3. Rate limiting
4. CSRF protection
5. Input sanitization

## Deployment Strategy

### Local Server Deployment

1. **Docker Compose** (Recommended):
   - Consistent environment
   - Easy updates
   - Auto-restart on failure

2. **Direct Python** (Development):
   - Faster iteration
   - Direct debugging
   - No containerization overhead

### Network Access

- **Local Only**: Bind to localhost (127.0.0.1)
- **Local Network**: Bind to 0.0.0.0, firewall rules
- **Internet**: Reverse proxy (nginx), HTTPS, authentication

## Performance Considerations

### Database

- SQLite adequate for family use (<100 transactions/day)
- Indexes on foreign keys (automatic)
- Read-heavy workload (dashboards)

### Caching

Currently none; future options:
- Browser caching for static assets
- Redis for session data
- Memoization for expensive queries

## Maintenance & Updates

### Backup Strategy

1. **Database Backups**:
   ```bash
   cp ledgerdb.sqlite ledgerdb_backup_$(date +%Y%m%d).sqlite
   ```

2. **Automated Backups**:
   - Cron job for daily backups
   - Keep 30 days of history

### Update Process

1. Pull new code
2. Run tests
3. Rebuild Docker image
4. Deploy with docker-compose

### Monitoring

- Docker health checks
- Application logs
- Disk space monitoring

## Future Enhancements

### Phase 2 Features

1. **Reporting**:
   - Charts/graphs (Chart.js)
   - Export to CSV/PDF
   - Monthly summaries

2. **Authentication**:
   - Parent login
   - Child view-only accounts

3. **Mobile App**:
   - Progressive Web App (PWA)
   - Push notifications

4. **Gamification**:
   - Badges for milestones
   - Savings goals
   - Reward streaks

5. **Multi-currency**:
   - Support for different currencies
   - Exchange rates

6. **API Expansion**:
   - Full REST API
   - Webhooks
   - Third-party integrations

## Code Standards

### Python Style

- PEP8 compliance
- Type hints on all functions
- Docstrings (Google style)
- Max line length: 88 (Black default)
- Max file length: 500 lines

### Documentation

- Inline comments for complex logic
- README for setup/usage
- PLANNING.md for architecture
- TASK.md for development tracking

### Version Control

- Meaningful commit messages
- Feature branches
- Pull request reviews (if team)

## Lessons Learned

1. **Start Simple**: MVP first, then enhance
2. **Test Early**: Write tests alongside features
3. **Documentation**: Essential for future maintenance
4. **Backward Compatibility**: Preserve existing data
5. **User Feedback**: Iterate based on family use

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Pytest Documentation](https://docs.pytest.org/)


