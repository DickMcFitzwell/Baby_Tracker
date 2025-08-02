CREATE TABLE IF NOT EXISTS bath (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
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
    progress TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS diaper (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    excrement TEXT NOT NULL,
    color TEXT,
    consistency TEXT,
    rash_level INTEGER NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    regular_checkup TEXT NOT NULL,
    symptom TEXT,
    height INTEGER,
    weight INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS medicine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    medicine TEXT NOT NULL,
    dose TEXT NOT NULL,
    reason TEXT,
    notes TEXT,
    effectiveness TEXT,
    final_notes TEXT
);

CREATE TABLE IF NOT EXISTS milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    milestone TEXT NOT NULL,
    notes TEXT NOT NULL
);