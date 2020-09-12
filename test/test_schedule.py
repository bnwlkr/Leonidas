import aiounittest
import pathlib

from leonidas import schedule, course


class TestSchedule(aiounittest.AsyncTestCase):  
    async def test_get_courses(self):
        test_data_dir = pathlib.Path(__file__).parent.joinpath('data')
        with open(test_data_dir.joinpath('schedule.ics'), 'r') as schedule_file:
            ics_txt = schedule_file.read()
        expected = {course.Course('CPSC', '415', '101'),
                    course.Course('CPSC', '417', '101'),
                    course.Course('CPSC', '418', '1W1'),
                    course.Course('BIOL', '112', 'T02'),
                    course.Course('BIOL', '112', '103'),
                    course.Course('BIOL', '121', '221'),
                    course.Course('BIOL', '200', '201'),
                    course.Course('CPSC', '425', '201'),
                    course.Course('CPSC', '445', '201'),
                    course.Course('CPSC', '416', '2W1')}

        actual = {c async for c in schedule.get_courses(ics_txt)}
        self.assertEqual(actual, expected)
