# library-management-system
FastAPI Library Management System with JWT Authentication, Book Management, Member Management, Book Issue &amp; Return, SQLAlchemy ORM, Search, Pagination, and Docker Support.
# Library Management System

## Features

- JWT Authentication
- Book Management
- Member Management
- Book Issue & Return
- Search & Filtering
- Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Setup Steps

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the project

```bash
uvicorn main:app --reload
```

## Environment Variables

```
SECRET_KEY=library_secret_key
ALGORITHM=HS256
```

## Authentication Flow

- Register using `/auth/register`
- Login using `/auth/login`
- JWT token is returned after successful login.

## API Flow

1. Register/Login
2. Add Books
3. Add Members
4. Issue Book
5. Return Book
6. View Member Borrowed Books

## Assumptions

- One member can borrow multiple books.
- Same member cannot borrow the same book twice without returning it.
- Books are soft deleted.
- Available copies are updated automatically.
