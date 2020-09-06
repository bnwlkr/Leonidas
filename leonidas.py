import os
import re
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

from leonidas import memory, speech, email, utils

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

EMAIL_REGEX = r"\b[\w.%+-]+@\w+\.ubc\.ca\b"

leonidas = commands.Bot('!')

@leonidas.event
async def on_ready():
    guild = discord.utils.get(leonidas.guilds, name=GUILD)
    if guild is None:
        raise LookupError(f"Guild '{GUILD}' not found")
    logging.info(f"{leonidas.user} connected to {guild.name}")


@leonidas.event
async def on_member_join(member):
    memory.users[member.id] = memory.User(member.id, member.name)
    await member.create_dm()
    await member.dm_channel.send(speech.GREETING % member.name)
    await member.dm_channel.send(speech.EMAIL_REQUEST)

@leonidas.event
async def on_message(msg):
    if msg.author == leonidas.user:
        return
    if isinstance(msg.channel, discord.DMChannel):  # process DM
        user = memory.users.get(msg.author.id)
        if user is None:
            logging.info(f"{msg.author}: {msg.content} (UNKNOWN)")
            return
        logging.info(f"{user}: {msg.content}")
        if user.verified:
            await msg.author.send(speech.ALREADY_VERIFIED)
            return
        email_search = re.search(EMAIL_REGEX, msg.content)
        if user.code is not None and user.code in msg.content:
            await msg.author.send(speech.VERIFIED)
            user.verified = True
            logging.info(f"{user} verified")
        elif user.code is not None and email_search is None:
            await msg.author.send(speech.BAD_CODE)
        elif user.code is None and email_search is None:
            await msg.author.send(speech.BAD_EMAIL)
        elif email_search is not None:
            email_addr = email_search.group()
            code = utils.generate_code()
            email_cfg = email.EmailConfig(EMAIL_ACCOUNT, EMAIL_PASSWD,
                                          EMAIL_SERVER_ADDR, EMAIL_SERVER_PORT)
            email.send_code(email_cfg, email_addr, code)
            user.code = code
            user.email = email_addr
            await msg.author.send(speech.SENT_EMAIL % email_addr)
    else:
        await leonidas.process_commands(msg)

# example of a command
@leonidas.command()
async def example(ctx, arg):
    print(f"{ctx.author}: !example {arg}")

def main():
    with memory.boot('memory.db'):
        leonidas.run(TOKEN)


if __name__ == '__main__':
    main() 
