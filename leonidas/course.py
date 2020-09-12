import itertools
from datetime import datetime

from leonidas import utils

class NoSuchCourseException(Exception):
    pass


class Course:
    """ Represents a university course

    Attributes:
        dept (str): e.g. 'CPSC', 'BIOL'
        code (str): e.g. '110', '415', '448B'
        section (str): e.g. '101', '2W1', 'L11'
    """
    @classmethod
    async def create(cls, dept, code, section=None):
        course = Course(dept, code, section)
        await course._validate()
        return course

    def __init__(self, dept, code, section=None):
        self.dept = dept.upper()
        self.code = code.upper()
        if section is not None:
            self.section = section.upper()
        else:
            self.section = None

    async def _validate(self):
        courses_url = 'https://courses.students.ubc.ca/cs/courseschedule?'
        params = {'pname': 'subjarea', 'dept': self.dept, 'course': self.code}
        if self.section:
            params['tname'] = 'subj-section'
            params['section'] = self.section
        else:
            params['tname'] = 'subj-course'
        page_contents = await utils.fetch(courses_url, params=params)
        if 'no longer offered' in page_contents:
            raise NoSuchCourseException()

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return self.dept == other.dept and \
               self.code == other.code

    def __hash__(self):
        return hash((self.dept,
                     self.code))

    def  __repr__(self):
        result = f"{self.dept} {self.code}"
        if self.section is not None:
            result = f"{result} {self.section}"
        return result

