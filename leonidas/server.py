import logging

import discord

from leonidas import email

async def create_channels(guild, course):
    secret = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    course_channel_name = f'{course.subj}-{course.code}'.lower()

    course_channel = discord.utils.get(guild.channels,
                                       name=course_channel_name)
    if course_channel is None:
        course_channel = await guild.create_text_channel(course_channel_name,
                                                         overwrites=secret)
        logging.info(f"created channel {course_channel} ({len(guild.channels)})")
    return course_channel


async def in_channel(user, channel):
    user_perms = channel.permissions_for(user)
    return user_perms.read_messages and user_perms.send_messages


async def add_to_channel(user, channel):
    logging.info(f"adding {user} to {channel}")
    await channel.set_permissions(user, read_messages=True, send_messages=True)


async def rm_from_channel(user, channel):
    logging.info(f"removing {user} from {channel}")
    await channel.set_permissions(user, read_messages=False)
