import aiounittest

from leonidas import course


class TestCourse(aiounittest.AsyncTestCase):
    async def test_create_valid_course(self):
        await course.Course.create('CPSC', 110)

    async def test_create_invalid_code(self):
        with self.assertRaises(course.NoSuchCourseException):
            await course.Course.create('CPSC', 610)

    async def test_create_valid_section(self):
        await course.Course.create('CPSC', 110, '101')

    async def test_create_invalid_section(self):
        with self.assertRaises(course.NoSuchCourseException):
           await course.Course.create('CPSC', 110, 'potato')

