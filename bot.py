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
import asyncio
import asyncpg
import discord
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


async def get_prefix(bot: commands.Bot, message: discord.Message):
    """Fetches the custom prefix for the provided guild."""

    if not message.guild:
        return CONFIG['defaultPrefix']

    guild_id = message.guild.id

    prefix = await bot.db.fetchrow(
        "select prefix from guilds where guild_id = $1",
        guild_id
    )

    if not prefix:
        async with bot.db.acquire() as conn:
            await conn.execute("insert into guilds (guild_id, prefix) values ($1, $2)",
                               guild_id, CONFIG['defaultPrefix'])
        return CONFIG["defaultPrefix"]

    return prefix[0]


bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    case_insensitive=True
)


async def database_setup():
    """Creates a database pool connection."""

    bot.db = await asyncpg.create_pool(
        user=USER,
        password=PASSWORD,
        database=NAME,
        host=HOSTNAME
    )

asyncio.get_event_loop().run_until_complete(database_setup())


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
