from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from models.user import User
from models.book import Book
from models.member import Member
from models.issue import Issue

from routes.auth import router as auth_router
from routes.books import router as books_router
from routes.members import router as members_router
from routes.issues import router as issues_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(books_router)
app.include_router(members_router)
app.include_router(issues_router)


@app.get("/")
def home():

    return {
        "message":
        "Library Management System"
    }
