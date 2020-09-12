import aiounittest

from leonidas import utils
from leonidas.course import Course


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

    async def test_find_courses_found(self):
        msg = "Please add me to CPSC 110"
        expected = {Course('CPSC', '110')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    async def test_find_courses_section(self):
        msg = "Please add me to CPSC 110 101"
        expected = {Course('CPSC', '110', section='101')}
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, expected)

    async def test_find_courses_empty(self):
        msg = "I hate squirrels"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, set())

    async def test_find_courses_invalid_course(self):
        msg = "I would like to be added to ALND 110 201"
        actual = {c async for c in utils.find_courses(msg)}
        self.assertSetEqual(actual, {"ALND 110 201"})


