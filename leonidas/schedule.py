import re
import logging

from leonidas import course, utils


async def find_courses(ics_txt, only_year=None):
    """Parses courses from the contents of a .ics file
    
    Args:
        ics_txt: The text contents of an .ics file
    Returns:
        A list of course.Course objects found
    """

    for line in ics_txt.splitlines():
        summary_search = re.search(r'SUMMARY:(.+)', line)
        if summary_search is not None:
            course_str = summary_search.group(1)
        year_search = re.search(r'DTSTART;.*:(\d{4})', line)
        if year_search is not None:
            year = int(year_search.group(1))
            if only_year is None or year == only_year:
                match = [c async for c in utils.find_courses(course_str)][0]
                if isinstance(match, course.Course):
                    yield match
                else:
                    logging.info(f"ics invalid course: {match}")
