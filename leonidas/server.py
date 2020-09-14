import logging

import discord


async def create_channels(guild, subjs_category, course):
    """Creates channels for `course` that don't already exist.

    Makes sure that there is a subject (e.g. CPSC) category 
    with a general text channel and a text channel for the given course. 
    If `course` has a section, also creates a section-specific channel.

    Args:
        guild: the guild (server) to create the channels in
        course: the `leonidas.course.Course` to create channels for
    Yields:
        - subject general channel
        - course channel
        - section channel (maybe)
    """
    secret = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    subj_general_name = course.subj.lower()
    subj_general = discord.utils.get(subjs_category.channels,
                                     name=subj_general_name)
    if subj_general is None:
        subj_general = await subjs_category.create_text_channel(subj_general_name,
                                                                overwrites=secret)
        logging.info(f"created channel {subj_general}")
    yield subj_general


    course_channel_name = f'{course.subj}-{course.code}'.lower()
    course_category = discord.utils.get(guild.categories,
                                        name=course_channel_name)
    if course_category is None:
        course_category = await guild.create_category(course_channel_name,
                                                      overwrites=secret)
        logging.info(f"created category {course_category}")


    course_channel = discord.utils.get(course_category.channels,
                                       name=course_channel_name)
    if course_channel is None:
        course_channel = await course_category.create_text_channel(course_channel_name,
                                                                   overwrites=secret)
        logging.info(f"created channel {course_channel}")
    yield course_channel


    if course.section is not None:
        section_channel_name = f'{course.subj}-{course.code}-{course.section}'.lower()
        section_channel = discord.utils.get(course_category.channels,
                                            name=section_channel_name)
        if section_channel is None:
            section_channel = await course_category.create_text_channel(section_channel_name,
                                                                        overwrites=secret)
            logging.info(f"created channel {section_channel}")
        yield section_channel


async def in_channel(user, channel):
    user_perms = channel.permissions_for(user)
    return user_perms.read_messages and user_perms.send_messages


async def add_to_channel(user, channel):
    logging.info(f"adding {user} to {channel}")
    await channel.set_permissions(user, read_messages=True, send_messages=True)


async def rm_from_channel(user, channel):
    logging.info(f"removing {user} from {channel}")
    await channel.set_permissions(user, read_messages=False, send_messages=False)
