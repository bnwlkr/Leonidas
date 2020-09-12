import re
import logging

from leonidas import course, utils


async def get_courses(ics_txt):
    """Parses courses from the contents of a .ics file
    
    Args:
        ics_txt: The text contents of an .ics file
    Returns:
        A list of course.Course objects found
    """
    for event_summary in re.finditer(r'SUMMARY:(.+)', ics_txt):
        course_txt = event_summary.group()
        match = [c async for c in utils.find_courses(course_txt)][0]
        if isinstance(match, course.Course):
            yield match
        else:
            logging.info(f"ics invalid course: {match}")
