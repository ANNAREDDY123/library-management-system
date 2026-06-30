from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from database import Base


class Issue(Base):
    __tablename__ = "issues"

    id = Column(
        Integer,
        primary_key=True
    )

    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    book_id = Column(
        Integer,
        ForeignKey("books.id")
    )

    issue_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    return_date = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String,
        default="Issued"
    )
