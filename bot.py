"""
bot.py
basic initialization and configuration of the bot
- loads external files - .env, .json
- sets up database connection
- loads cogs and prefixes
- creates bot instance
"""

import os
import json
import dotenv
import logging
from discord.ext import commands


# loads environment variables
dotenv.load_dotenv()
TOKEN = os.getenv('discord_token')
DBL_TOKEN = os.getenv('dbl_token')
AUTH = os.getenv('dbl_auth')
HOSTNAME = os.getenv('database_hostname')
NAME = os.getenv('database_name')
USER = os.getenv('database_user')
PASSWORD = os.getenv('database_password')


with open('data/config.json') as CONFIG:
    CONFIG = json.load(CONFIG)


bot = commands.AutoShardedBot(
    command_prefix=CONFIG['defaultPrefix'],
    case_insensitive=True
)


logging.basicConfig(
    filename='discord.log',
    level=logging.INFO
)

bot.config = CONFIG

bot.cog_list = [
    'cogs.core.database',
    'cogs.core.settings',
    'cogs.commands.commands',
    'cogs.commands.events',
    'cogs.commands.moderation',
    'cogs.commands.owner',
    'cogs.commands.utility'
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(TOKEN)
