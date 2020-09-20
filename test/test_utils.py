import mock
import aiounittest

from leonidas import utils, course


class TestUtils(aiounittest.AsyncTestCase):
    def test_find_email_found(self):
        msg = "Hello, my email is test@alumni.ubc.ca"
        expected = 'test@alumni.ubc.ca'
        actual = utils.find_email(msg)
        self.assertEqual(actual, expected)

    def test_find_email_none(self):
        msg = "Hello, what is an email?"
        actual = utils.find_email(msg)
        self.assertIsNone(actual)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_found_space(self, _validate_mock):
        msg = "CPSC 110, CPSC415, AANB 530A"
        expected = {course.Course('CPSC', '110'),
                    course.Course('CPSC', '415'),
                    course.Course('AANB', '530A')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    @mock.patch('leonidas.course.Course._validate')
    async def test_find_courses_empty(self, _validate_mock):
        msg = "I hate squirrels"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, set())

    async def test_find_courses_invalid_course(self):
        msg = "I would like to be added to ALND 110"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, {"ALND 110"})


