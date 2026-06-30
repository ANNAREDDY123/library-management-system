from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.member import Member

from schemas.member import MemberCreate

from services.library_service import valid_phone

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Member).filter(
        Member.email == member.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if not valid_phone(member.phone):

        raise HTTPException(
            status_code=400,
            detail="Invalid phone number"
        )

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        is_active=member.is_active
    )

    db.add(new_member)

    db.commit()

    db.refresh(new_member)

    return new_member


@router.get("/")
def get_members(
    db: Session = Depends(get_db)
):

    return db.query(Member).all()


@router.get("/{member_id}")
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member
