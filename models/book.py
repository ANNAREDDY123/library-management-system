from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(String)

    author = Column(String)

    category = Column(String)

    isbn = Column(
        String,
        unique=True
    )

    total_copies = Column(Integer)

    available_copies = Column(Integer)

    is_active = Column(
        Boolean,
        default=True
    )
