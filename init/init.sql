CREATE TABLE IF NOT EXISTS entity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_income REAL,
    age INTEGER,
    full_name TEXT,
    phone TEXT,
    email TEXT,
    category TEXT,
    balance REAL
);