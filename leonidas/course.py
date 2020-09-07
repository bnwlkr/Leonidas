import requests
import itertools
from datetime import datetime

class NoSuchCourseException(Exception):
    pass


class Course:
    """ Represents a university course

    Attributes:
        year (int): e.g. 2019, 2020
        session (str): 'S' or 'W'
        dept (str): e.g. 'CPSC', 'BIOL'
        code (int): e.g. 110, 415
        section (str): e.g. '101', '2W1'
    """
    def __init__(self, dept, code):
        self.dept = dept
        self.code = code
        self._validate()


    def _validate(self):
        courses_url = 'https://courses.students.ubc.ca/cs/courseschedule?'
        params = {'pname': 'subjarea', 'tname': 'subj-course',
                  'dept': self.dept, 'course': self.code}
        result = requests.get(courses_url, params).text
        if 'no longer offered' in result:
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
        return f"{self.dept} {self.code}"


