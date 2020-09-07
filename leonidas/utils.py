import re
import random, string

from leonidas import course

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def find_email(msg):
    regex = r"\b[\w.%+-]+@\w+\.ubc\.ca\b"
    search = re.search(regex, msg)
    if search is not None:
        return search.group()
    else:
        return None

def find_courses(msg):  # TODO: make me async!
    regex = r"\b(?P<dept>[A-z]{4}) (?P<code>\d{1,4})\b"
    result = set()
    for match in re.finditer(regex, msg):
        try:
            match_dict = match.groupdict()
            found_course = course.Course(match_dict['dept'], int(match_dict['code']))
            result.add(found_course)
        except course.NoSuchCourseException:
            logging.info(f"invalid course: {match_dict['dept']} "
                          "{match_dict['code']}")
    return result

    

