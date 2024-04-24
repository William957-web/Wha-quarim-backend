DROP TABLE IF EXISTS fish;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS food;

CREATE TABLE fish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER,
    hunger INTEGER,
    long INTEGER,
    food_time INTEGER
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    fishes TEXT,
    foods TEXT,
    money INTEGER,
    play INTEGER,
    pre_fishes TEXT,
    achieve TEXT,
    token TEXT
);

CREATE TABLE food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER,
    power INTEGER
);