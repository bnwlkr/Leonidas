import sqlite3
from enum import Enum
from contextlib import contextmanager

class Stage(Enum):
    EMAIL = 'email'
    CODE = 'code'
    VERIFIED = 'verified'

user_stage = {}
user_code = {}
user_email = {}

@contextmanager
def boot(db_path):
    with sqlite3.connect(db_path) as db_conn:
        _populate_memory(db_conn)
        try:
            yield
        finally:
            _write_memory(db_conn)


def _populate_memory(db_conn):
    print("populate memory")
    pass

def _write_memory(db_conn):
    print("write memory")
    pass
