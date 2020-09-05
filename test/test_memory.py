import sqlite3
import unittest

from leonidas import memory

class TestMemory(unittest.TestCase):
    def run(self, result=None):
        with memory.boot('memory.db'):
            super(TestMemory, self).run(result)

