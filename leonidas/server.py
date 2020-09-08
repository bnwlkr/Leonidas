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
    """
    logging.info(f"creating channels for {course}")
    perm_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    if discord.utils.get(guild.categories, name=course.dept) is None:
        dept_category = await guild.create_category(course.dept,
                                                    overwrites=perm_overwrites)
        logging.info(f"created department category {dept_category}")
        dept_general = await dept_category.create_text_channel('general')
        logging.info(f"created {dept_category} general channel")


