import re
import logging
import random, string

from leonidas.course import Course, NoSuchCourseException

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def find_email(msg):
    regex = r"\b[\w.%+-]+@\w+\.ubc\.ca\b"
    search = re.search(regex, msg)
    if search is not None:
        return search.group()
    else:
        return None

async def find_courses(msg):
    regex = (r"\b(?P<dept>[A-z]{3,4}) "
             r"(?P<code>[\dA-z]{3,4})"
             r"(?: (?P<section>[\dA-z]{3}))?\b")
    print(regex, msg)
    for match in re.finditer(regex, msg):
        print(match)
        try:
            match_dict = match.groupdict()
            course = await Course.create(match_dict['dept'],
                                         int(match_dict['code']),
                                         section=match_dict['section'])
            yield course
        except NoSuchCourseException:
            logging.info(f"invalid course: {match_dict['dept']} "
                          "{match_dict['code']}")
            no_match_resp = f"{match_dict['dept']} {match_dict['code']}"
            if match_dict['section'] is not None:
                no_match_resp = f"{no_match_resp} {match_dict['section']}"
            yield no_match_resp

