#!/home/bnwlkr/Leonidas/ven2/bin/python3.8

import os
import re
import logging
import asyncio

from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from leonidas import memory, speech, email, utils, course, server

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWD = os.getenv('EMAIL_PASSWD')
EMAIL_SERVER_ADDR = os.getenv('EMAIL_SERVER_ADDR')
EMAIL_SERVER_PORT = os.getenv('EMAIL_SERVER_PORT')

assert TOKEN and GUILD and EMAIL_ACCOUNT and \
EMAIL_PASSWD and EMAIL_SERVER_ADDR and EMAIL_SERVER_PORT

EMAIL_SERVER_PORT = int(EMAIL_SERVER_PORT)

logging.basicConfig(level=logging.INFO)

bot = commands.Bot('!')

@bot.event
async def on_ready():
    global guild
    global general_channel
    global help_channel

    guild = discord.utils.get(bot.guilds, name=GUILD)
    assert guild is not None, f"couldn't find guild {GUILD}"

    help_channel = discord.utils.get(guild.channels, name='help')
    assert help_channel is not None, "couldn't find help channel"

    general_channel = discord.utils.get(guild.channels, name='general')
    assert general_channel is not None, "couldn't find general channel"

    logging.info(f"{bot.user} connected to {guild.name}")


async def handle_course_request(user, course):
    logging.info(f"course request for {course}")
    member = guild.get_member(user.id)
    added_to_channel = False
    channel = await server.create_channels(guild, course)
    if not (await server.in_channel(member, channel)):
        await server.add_to_channel(member, channel)
        added_to_channel = True
        await member.dm_channel.send(speech.ADDED_TO_CHANNEL % channel.id)

    if not added_to_channel:
        await member.dm_channel.send(speech.ALREADY_IN_CHANNELS % course)


@bot.event
async def on_member_join(member):
    memory.users[member.id] = memory.User(member.id, member.name)
    await member.create_dm()
    await member.dm_channel.send(speech.GREETING % (member.name, bot.user.id))
    await member.dm_channel.send(speech.EMAIL_REQUEST)
    await member.dm_channel.send(embed=speech.EMAIL_INST_EMBED)
    logging.info(f"new member {member.name}")


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if isinstance(msg.channel, discord.DMChannel):
        guild_member = guild.get_member(msg.author.id)
        user = memory.users.get(msg.author.id)

        if guild_member == guild.owner:
            logging.info("message from admin")
            msg_search = re.search(r'<(?P<channel>[A-z\d\-]+)> (?P<msg>.+)', msg.content)
            if msg_search is not None:
                match_dict = msg_search.groupdict()
                channel = discord.utils.get(guild.channels, name=match_dict['channel'])
                await channel.send(match_dict['msg'])
                logging.info(f"manually sent message in {channel}")
                return

        if guild_member is None:
            await msg.author.send(speech.UNKNOWN_USER % help_channel.create_invite())
            return

        if user is None:
            logging.info(f"{msg.author} ({msg.author.id}): {msg.content} (UNKNOWN)")
            memory.users[msg.author.id] = memory.User(msg.author.id, msg.author.name)
            await msg.author.send(speech.RE_VERIFY % msg.author.name)
            await msg.author.send(speech.EMAIL_REQUEST)
            return

        logging.info(f"{user}: {msg.content}")

        if user.verified:

            if 'help' in msg.content.lower():
                logging.info("verified asking for help")
                await msg.author.send(speech.COURSE_INSTRUCTIONS_1)
                await msg.author.send(speech.COURSE_INSTRUCTIONS_2)
                return

            leave_search = re.search(r'leave ([A-z\d\-]+)', msg.content.lower())
            if leave_search is not None:
                channel_name = leave_search.group(1)
                channel = discord.utils.get(guild.channels, name=channel_name)
                if channel_name in ['general', 'help']:
                    channel = None
                if channel is not None:
                    await server.rm_from_channel(guild_member, channel)
                    await msg.author.send(speech.REMOVED_FROM_CHANNEL % channel)
                else:
                    await msg.author.send(speech.INVALID_CHANNEL %
                                          (channel_name, help_channel.id))
                return

            found_course = False
            msg_matches = {m async for m in utils.find_courses(msg.content)}
            for msg_match in msg_matches:
                if isinstance(msg_match, course.Course):
                    found_course = True
                    await handle_course_request(msg.author, msg_match)
                else:
                    await msg.author.send(speech.BAD_COURSE % msg_match)

            if not found_course:
                await msg.author.send(speech.NO_COURSES % help_channel.id)
            return

        if 'help' in msg.content.lower():
            logging.info("unverified asking for help")
            await msg.author.send(speech.EMAIL_REQUEST)
            await msg.author.send(embed=speech.EMAIL_INST_EMBED)
            return

        email_addr = utils.find_email(msg.content)
        if user.code is not None and user.code in msg.content:
            user.verified = True
            logging.info(f"{user} verified")
            await server.add_to_channel(guild_member, general_channel)
            await msg.author.send(speech.VERIFIED % general_channel.id)
            await msg.author.send(speech.COURSE_INSTRUCTIONS_1)
            await msg.author.send(speech.COURSE_INSTRUCTIONS_2)
        elif user.code is not None and email_addr is None:
            await msg.author.send(speech.BAD_CODE % help_channel.id)
        elif user.code is None and email_addr is None:
            await msg.author.send(speech.BAD_EMAIL % help_channel.id)
        elif email_addr:
            if memory.email_already_verified(email_addr):
                await msg.author.send(speech.EMAIL_ALREADY_USED % help_channel.id)
                logging.info(f"{user}: {email_addr} already used")
                return
            code = utils.generate_code()
            email_cfg = email.EmailConfig(EMAIL_ACCOUNT, EMAIL_PASSWD,
                                          EMAIL_SERVER_ADDR, EMAIL_SERVER_PORT)
            email.send_code(email_cfg, email_addr, code)
            user.code = code
            user.email = email_addr
            await msg.author.send(speech.SENT_EMAIL % email_addr)
    else:
        await bot.process_commands(msg)


def main():
    with memory.boot('memory.db'):
        bot.run(TOKEN)


if __name__ == '__main__':
    main()
