import logging

import discord

class CourseChannels:
    def __init__(self, dept_general, course_channel, section_channel=None):
        self.dept_general = dept_general
        self.course_channel = course_channel
        self.section_channel = section_channel

async def create_channels(guild, course):
    """Creates channels for `course` that don't already exist.

    Makes sure that there is a department (e.g. CPSC) category 
    with a general text channel and a text channel for the given course. 
    If `course` has a section, also creates a section-specific channel.

    Args:
        guild: the guild (server) to create the channels in
        course: the `leonidas.course.Course` to create channels for
    """
    logging.info(f"creating channels for {course}")
    secret = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    dept_category = discord.utils.get(guild.categories, name=course.dept)
    if dept_category is None:
        dept_category = await guild.create_category(course.dept,
                                                    overwrites=secret)
        logging.info(f"created department category {dept_category}")
    dept_general = discord.utils.get(dept_category.channels, name='general')
    if dept_general is None:
        dept_general = await dept_category.create_text_channel('general')
        logging.info(f"created {dept_category} general channel")
    course_channel_name = f"{course.dept}-{course.code}".lower()
    course_channel = discord.utils.get(dept_category.channels, name=course_channel_name)
    if course_channel is None:
        course_channel = await dept_category.create_text_channel(course_channel_name,
                                                                 overwrites=secret)
        logging.info(f"created course channel {course_channel}")
    section_channel = None
    if course.section is not None:
        section_channel_name = f"{course.dept}-{course.code}-{course.section}".lower()
        section_channel = discord.utils.get(dept_category.channels, name=section_channel_name)
        if section_channel is None:
            section_channel = await dept_category.create_text_channel(section_channel_name,
                                                                      overwrites=secret)
            logging.info(f"created section channel {section_channel}")
    return CourseChannels(dept_general, course_channel, section_channel=section_channel)

