CREATE TABLE IF NOT EXISTS diaper (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    excrement TEXT NOT NULL,
    color TEXT,
    consistency TEXT,
    rash_level INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS bottle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    duration TEXT,
    ounces FLOAT NOT NULL,
    contents TEXT,
    notes TEXT
);