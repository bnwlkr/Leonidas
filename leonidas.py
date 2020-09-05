import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

leonidas = commands.Bot('!')

def is_already_verified(user):
    return False


@leonidas.event
async def on_ready():
    guild = discord.utils.get(leonidas.guilds, name=GUILD)
    if guild is None:
        raise LookupError(f"Guild '{GUILD}' not found")
    print(f"{leonidas.user} connected to {guild.name}")


@leonidas.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, I am leonidas, The Guardian."
         "I'm here to make sure you don't go to SFU."
    )
    await member.dm_channel.send(
        f"What's your UBC email address? (ends with alumni.ubc.ca)"
    )

@leonidas.event
async def on_message(message):
    if message.author == leonidas.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        print(f"{message.author}: {message.content}")


def main():
    leonidas.run(TOKEN)



if __name__ == '__main__':
    main() 
