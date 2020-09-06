import logging
import sqlite3
from enum import Enum
from contextlib import contextmanager

users = {}

class User():
    def __init__(self, id, name, verified=False, code=None, email=None):
        self.id = id
        self.name = name
        self.verified = verified
        self.code = code
        self.email = email

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return self.id

    def __str__(self):
        return (f"{self.name} {self.verified} "
                f"{self.code} {self.email}")

@contextmanager
def boot(db_path):
    with sqlite3.connect(db_path) as db_conn:
        db_cursor = db_conn.cursor()
        _read(db_cursor)
        try:
            yield
        finally:
            _write(db_cursor)


def _read(db_cursor):
    logging.info("read memory")
    db_users = db_cursor.execute("SELECT id, name, verified, email "
                                  "FROM users").fetchall()
    for db_user in db_users:
        id = db_user[0]
        users[id] = User(id, db_user[1], bool(db_user[2]), db_user[3])

def _write(db_cursor):
    logging.info("write memory")
    try:
        _create_db(db_cursor)
    except sqlite3.OperationalError:
        pass

    for user in users.values():
        db_cursor.execute("UPDATE users "
                          "SET name = ?, verified = ?, code = ?, email = ? "
                          "WHERE id = ?",
                          [user.name, user.verified,
                           user.code, user.email, user.id])
        if db_cursor.rowcount == 0:
            db_cursor.execute("INSERT INTO users (id, name, verified, code, email) "
                              "VALUES (?, ?, ?, ?, ?)", 
                              [user.id, user.name, user.verified,
                               user.code, user.email])


def _create_db(db_cursor):
    db_cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            verified INTEGER,
            code VARCHAR(32),
            email VARCHAR(255)
        )
        """
    )
    logging.info("created memory database")
