import re
import logging
import random
import string
import aiohttp

from leonidas import course

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def find_email(msg):
    regex = r"\b[\w.%+-]+@(.+\.)?ubc\.ca\b"
    search = re.search(regex, msg)
    if search is not None:
        return search.group()
    else:
        return None

async def find_courses(msg):
    regex = (r"\b(?P<subj>[A-z]{3,4})[\s-]?"
             r"(?P<code>[\dA-z]{3,4})\b")
    for match in re.finditer(regex, msg):
        try:
            match_dict = match.groupdict()
            found_course = await course.Course.create(match_dict['subj'],
                                                      match_dict['code'])
            yield found_course
        except course.NoSuchCourseException:
            logging.info(f"invalid course: {match_dict['subj']} "
                         f"{match_dict['code']}")
            no_match_resp = f"{match_dict['subj']} {match_dict['code']}"
            yield no_match_resp

async def fetch(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.text()
