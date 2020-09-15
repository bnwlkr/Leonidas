import os
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWD = os.getenv('EMAIL_PASSWD')
EMAIL_SERVER_ADDR = os.getenv('EMAIL_SERVER_ADDR')
EMAIL_SERVER_PORT = os.getenv('EMAIL_SERVER_PORT')

assert TOKEN and GUILD and EMAIL_ACCOUNT and \
       EMAIL_PASSWD and EMAIL_SERVER_ADDR and EMAIL_SERVER_PORT

SCHEDULE_YEAR = os.getenv('SCHEDULE_YEAR', default=None)

EMAIL_SERVER_PORT = int(EMAIL_SERVER_PORT)
SCHEDULE_YEAR = int(SCHEDULE_YEAR)

logging.basicConfig(level=logging.INFO)
