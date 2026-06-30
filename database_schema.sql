CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE books(
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    category VARCHAR(100),
    isbn VARCHAR(100) UNIQUE,
    total_copies INTEGER,
    available_copies INTEGER,
    is_active BOOLEAN
);

CREATE TABLE members(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    is_active BOOLEAN
);

CREATE TABLE issues(
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    book_id INTEGER,
    issue_date DATETIME,
    return_date DATETIME,
    status VARCHAR(50)
);
