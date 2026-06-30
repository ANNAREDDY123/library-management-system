from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import datetime

from database import SessionLocal

from models.issue import Issue
from models.book import Book
from models.member import Member

from schemas.issue import IssueCreate

router = APIRouter(
    tags=["Book Issues"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/issues")
def issue_book(
    issue: IssueCreate,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(
        Member.id == issue.member_id
    ).first()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    book = db.query(Book).filter(
        Book.id == issue.book_id
    ).first()

    if not book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.available_copies <= 0:

        raise HTTPException(
            status_code=400,
            detail="Book unavailable"
        )

    existing = db.query(Issue).filter(
        Issue.member_id == issue.member_id,
        Issue.book_id == issue.book_id,
        Issue.status == "Issued"
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Book already issued"
        )

    new_issue = Issue(
        member_id=issue.member_id,
        book_id=issue.book_id
    )

    db.add(new_issue)

    book.available_copies -= 1

    db.commit()

    db.refresh(new_issue)

    return new_issue


@router.put("/returns/{issue_id}")
def return_book(
    issue_id: int,
    db: Session = Depends(get_db)
):

    issue = db.query(Issue).filter(
        Issue.id == issue_id
    ).first()

    if not issue:

        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    if issue.status == "Returned":

        raise HTTPException(
            status_code=400,
            detail="Book already returned"
        )

    book = db.query(Book).filter(
        Book.id == issue.book_id
    ).first()

    book.available_copies += 1

    issue.status = "Returned"
    issue.return_date = datetime.utcnow()

    db.commit()

    return {
        "message": "Book returned successfully"
    }


@router.get("/members/{member_id}/books")
def member_books(
    member_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Issue).filter(
        Issue.member_id == member_id
    ).all()
