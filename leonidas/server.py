import logging

import discord


async def create_channels(guild, course):
    """Creates channels for `course` that don't already exist.

    Makes sure that there is a department (e.g. CPSC) category 
    with a general text channel and a text channel for the given course. 
    If `course` has a section, also creates a section-specific channel.

    Args:
        guild: the guild (server) to create the channels in
        course: the `leonidas.course.Course` to create channels for
    Yields:
        - department general channel
        - course channel
        - section channel (maybe)
    """
    secret = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    dept_category = discord.utils.get(guild.categories, name=course.dept)
    if dept_category is None:
        dept_category = await guild.create_category(course.dept,
                                                    overwrites=secret)
        logging.info(f"created department category {dept_category}")

    dept_general_name = f'{course.dept}-general'.lower()
    dept_general = discord.utils.get(dept_category.channels, name=dept_general_name)
    if dept_general is None:
        dept_general = await dept_category.create_text_channel(dept_general_name,
                                                               overwrites=secret)
        logging.info(f"created channel {dept_general}")
        yield dept_general

    course_channel_name = f"{course.dept}-{course.code}".lower()
    course_channel = discord.utils.get(dept_category.channels, name=course_channel_name)
    if course_channel is None:
        course_channel = await dept_category.create_text_channel(course_channel_name,
                                                                 overwrites=secret)
        logging.info(f"created channel {course_channel}")
        yield course_channel

    section_channel = None
    if course.section is not None:
        section_channel_name = f"{course.dept}-{course.code}-{course.section}".lower()
        section_channel = discord.utils.get(dept_category.channels,
                                            name=section_channel_name)
        if section_channel is None:
            section_channel = await dept_category.create_text_channel(section_channel_name,
                                                                      overwrites=secret)
            logging.info(f"created channel {section_channel}")
            yield section_channel


async def in_channel(user, channel):
    user_perms = channel.permissions_for(user)
    return user_perms.read_messages and user_perms.send_messages
        

async def add_to_channel(user, channel):
    logging.info(f"adding {user} to {channel}")
    await channel.set_permissions(user, read_messages=True, send_messages=True)

