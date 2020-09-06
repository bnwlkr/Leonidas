

class NoSuchCourseException(Exception):
    pass


class Course:
    """ Represents a university course

    Attributes:
        term (str): e.g. '2020W1'
        faculty (str): e.g. 'Science', 'Arts'
        dept (str): e.g. 'CPSC', 'BIOL'
        code (int): e.g. 110, 415
        section (str): e.g. '101', '2W1'
    """
    def __init__(self, term, faculty, dept, code, section=None):
        self.term = term
        self.faculty = faculty
        self.dept = dept
        self.code = code
        self.section = section
        self._validate()


    def _validate(self):
        raise NoSuchCourseException()

    def __eq__(self, other):
        if not isinstance(other, Class):
            return False
        return self.faculty == other.faculty and \
               self.dept == other.dept and \
               self.code == other.code and \
               self.section == other.section

    def __hash__(self):
        return hash((self.faculty,
                     self.dept,
                     self.code,
                     self.section))


