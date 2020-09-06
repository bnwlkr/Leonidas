import os
import sqlite3
import unittest
from unittest import mock
import logging
import copy

from leonidas import memory

class TestMemory(unittest.TestCase):


    def run(self, result=None):
        logging.basicConfig(level=logging.DEBUG)
        db_path = 'test/data/memory.db'
        if os.path.exists(db_path):
            os.remove(db_path)
        with sqlite3.connect(db_path) as db_conn:
            self.db_cursor = db_conn.cursor()
            memory._create_db(self.db_cursor)
            super(TestMemory, self).run(result)


    def setUp(self):
        memory.users = {}
        self.db_cursor.execute("DELETE FROM users")

    def test_write_read_new_user(self):
        user = memory.User(1, 'bnwlkr', False)
        memory.users[user.id] = user
        memory._write(self.db_cursor)
        memory.users = {}
        memory._read(self.db_cursor)
        self.assertDictEqual(memory.users, {1: user})
        

    def test_write_update_user(self):
        user = memory.User(1, 'bnwlkr', False)
        memory.users[user.id] = user
        memory._write(self.db_cursor)
        user.code = 'Vx57a8'
        user.email = 'benwalker@alumni.ubc.ca'
        memory._write(self.db_cursor)
        memory.users = {}
        memory._read(self.db_cursor)
        self.assertDictEqual(memory.users, {1: user})

