import re
import logging
import random
import string
import aiohttp

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

async def find_courses(msg):
    regex = (r"\b(?P<dept>[A-z]{3,4}) "
             r"(?P<code>[\dA-z]{3,4})"
             r"(?: (?P<section>[\dA-z]{3}))?\b")
    for match in re.finditer(regex, msg):
        try:
            match_dict = match.groupdict()
            found_course = await course.Course.create(match_dict['dept'],
                                                      match_dict['code'],
                                                      section=match_dict['section'])
            yield found_course
        except course.NoSuchCourseException:
            logging.info(f"invalid course: {match_dict['dept']} "
                         f"{match_dict['code']}")
            no_match_resp = f"{match_dict['dept']} {match_dict['code']}"
            if match_dict['section'] is not None:
                no_match_resp = f"{no_match_resp} {match_dict['section']}"
            yield no_match_resp

async def fetch(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.text()
