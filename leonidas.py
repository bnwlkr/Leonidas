import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

from leonidas import memory, utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


EMAIL_REGEX = r"\b[\w.%+-]+@alumni\.ubc\.ca\b"

GREETING = ("Greetings %s, I am Leonidas. "
            "I'm here to make sure you don't go to SFU.")

EMAIL_REQUEST = ("Please tell me your UBC email address."
                 "It should end with @alumni.ubc.ca")

BAD_EMAIL = ("Hmm, I couldn't see a UBC email address in your message. "
             "Please try again.")

SENT_EMAIL = ("Thanks! I sent an email with an access code to %s."
              "Respond to me here with the code once you receive it.")


leonidas = commands.Bot('!')

@leonidas.event
async def on_ready():
    guild = discord.utils.get(leonidas.guilds, name=GUILD)
    if guild is None:
        raise LookupError(f"Guild '{GUILD}' not found")
    print(f"{leonidas.user} connected to {guild.name}")


@leonidas.event
async def on_member_join(member):
    memory.user_stage = memory.Stage.EMAIL
    await member.create_dm()
    await member.dm_channel.send(GREETING % member.name)
    await member.dm_channel.send(EMAIL_REQUEST)

@leonidas.event
async def on_message(msg):
    if msg.author == leonidas.user:
        return
    if isinstance(msg.channel, discord.DMChannel):  # process DM
        print(f"{msg.author}: {msg.content}")
        if memory.user_stage == memory.Stage.EMAIL:
            email_search = re.search(EMAIL_REGEX, msg.content)
            if email_search is None:
                await msg.author.send(BAD_EMAIL_RESP)
            else:
                email = email_search.group()
                print(f"parsed email: {email}")
                access_code = utils.generate_code()
                memory.user_email[msg.author] = email
                memory.user_stage[msg.author] = memory.Stage.CODE
                memory.user_code[msg.author] = access_code
                await msg.author.send(SENT_EMAIL % email)

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
