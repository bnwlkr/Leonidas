import unittest

from leonidas import utils, course

class TestUtils(unittest.TestCase):
    def test_find_email_found(self):
        msg = "Hello, my email is test@alumni.ubc.ca"
        expected = 'test@alumni.ubc.ca'
        actual = utils.find_email(msg)
        self.assertEqual(actual, expected)

    def test_find_email_none(self):
        msg = "Hello, what is an email?"
        actual = utils.find_email(msg)
        self.assertIsNone(actual)

    def test_find_courses_found(self):
        msg = "Please add me to CPSC 110"
        expected = {course.Course('CPSC', 110)}
        actual = utils.find_courses(msg)
        self.assertSetEqual(actual, expected)

    def test_find_courses_empty(self):
        msg = "I hate squirrels"
        actual = utils.find_courses(msg)
        self.assertSetEqual(actual, set())
