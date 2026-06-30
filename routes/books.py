from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.book import Book

from schemas.book import BookCreate

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Book).filter(
        Book.isbn == book.isbn
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    new_book = Book(
        title=book.title,
        author=book.author,
        category=book.category,
        isbn=book.isbn,
        total_copies=book.total_copies,
        available_copies=book.available_copies,
        is_active=book.is_active
    )

    db.add(new_book)

    db.commit()

    db.refresh(new_book)

    return new_book


@router.get("/")
def get_books(
    title: str = None,
    author: str = None,
    category: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    if author:
        query = query.filter(Book.author.contains(author))

    if category:
        query = query.filter(Book.category == category)

    total = query.count()

    books = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": books
    }


@router.get("/{book_id}")
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@router.put("/{book_id}")
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db)
):

    db_book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not db_book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db_book.title = book.title
    db_book.author = book.author
    db_book.category = book.category
    db_book.isbn = book.isbn
    db_book.total_copies = book.total_copies
    db_book.available_copies = book.available_copies
    db_book.is_active = book.is_active

    db.commit()

    return {
        "message":
        "Book updated"
    }


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.is_active = False

    db.commit()

    return {
        "message":
        "Book deactivated"
    }
