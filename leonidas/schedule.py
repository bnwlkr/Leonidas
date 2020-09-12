import re
import logging

from leonidas import course, utils

# Disabling ics parsing for now for the sake of simplicity.
# As is, it adds courses from both terms which makes things
# pretty cluttered. There are some solutions to this but I don't
# think that manually typing out courses is that much of a barrier.
# Once we get nested categories the clutter problem is solved.

# This is the part of leonidas.py that was running it before:
#
#  for attachment in msg.attachments:
#      if not attachment.filename.endswith('.ics'):
#          logging.info("non-ics file uploaded")
#          await msg.author.send(BAD_SCHEDULE)
#          return
#      ics_txt = await utils.fetch(attachment.url)
#      for parsed_course in {c async for c in
#                            schedule.get_courses(ics_txt)}:
#          found_course = True
#          await handle_course_request(msg.author, parsed_course)
# And a speech entry:
#
#  BAD_SCHEDULE = ("Hmm, that doesn't look like the right file format to me\n"
#                  + _HAVING_TROUBLE)


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
