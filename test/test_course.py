import unittest

from leonidas import course

class TestCourse(unittest.TestCase):
    def test_create_invalid_term(self):
        with self.assertRaises(course.NoSuchCourseException):
            pass

    def test_create_invalid_faculty(self):
        with self.assertRaises(course.NoSuchCourseException):
            pass

    def test_create_invalid_dept(self):
        with self.assertRaises(course.NoSuchCourseException):
            pass

    def test_create_invalid_code(self):
        with self.assertRaises(course.NoSuchCourseException):
            pass

    def test_create_invalid_section(self):
        with self.assertRaises(course.NoSuchCourseException):
            pass
