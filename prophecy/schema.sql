CREATE TABLE students (
    id INTEGER,
    student_name TEXT,
    house_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(house_id) REFERENCES houses(id)
);

CREATE TABLE houses (
    id INTEGER,
    name TEXT,
    head TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE assignments (
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
);