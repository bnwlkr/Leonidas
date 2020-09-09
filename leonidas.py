import os
import re
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

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


async def handle_course_request(user, course):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    assert guild is not None, f"couldn't find guild {GUILD}"
    course_channels = await server.create_channels(guild, course)
    print(course_channels)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    assert guild is not None, f"couldn't find guild {GUILD}"
    logging.info(f"{bot.user} connected to {guild.name}")


@bot.event
async def on_member_join(member):
    memory.users[member.id] = memory.User(member.id, member.name)
    await member.create_dm()
    await member.dm_channel.send(speech.GREETING % member.name)
    await member.dm_channel.send(speech.EMAIL_REQUEST)

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if isinstance(msg.channel, discord.DMChannel):  # process DM
        user = memory.users.get(msg.author.id)
        if user is None:
            logging.info(f"{msg.author} ({msg.author.id}): {msg.content} (UNKNOWN)")
            return
        logging.info(f"{user}: {msg.content}")
        if user.verified:
            found_course = False
            async for match in utils.find_courses(msg.content):
                if isinstance(match, course.Course):
                    found_course = True
                    await handle_course_request(msg.author, match)
                else:
                    await msg.author.send(speech.BAD_COURSE % match)
            if not found_course:
                await msg.author.send(speech.NO_COURSES)
            return
        email_addr = utils.find_email(msg.content)
        if user.code is not None and user.code in msg.content:
            await msg.author.send(speech.VERIFIED)
            user.verified = True
            logging.info(f"{user} verified")
        elif user.code is not None and email_addr is None:
            await msg.author.send(speech.BAD_CODE)
        elif user.code is None and email_addr is None:
            await msg.author.send(speech.BAD_EMAIL)
        elif email_addr:
            if memory.email_already_verified(email_addr):
                await msg.author.send(speech.EMAIL_ALREADY_USED)
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

# example of a command
@bot.command()
async def example(ctx, arg):
    print(f"{ctx.author}: !example {arg}")

def main():
    with memory.boot('memory.db'):
        bot.run(TOKEN)


if __name__ == '__main__':
    main() 
