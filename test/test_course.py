import unittest

from leonidas import course

class TestCourse(unittest.TestCase):
    def test_create_invalid_session(self):
        with self.assertRaises(course.NoSuchCourseException):
            course.Course('CPSC', 610)

    def test_create_valid(self):
        course.Course('CPSC', 110)
