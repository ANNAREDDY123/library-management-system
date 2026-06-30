from pydantic import BaseModel


class IssueCreate(BaseModel):

    member_id: int

    book_id: int
