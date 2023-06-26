import os
import logging
import disnake
import asyncio

from constants import *
from util import errors
from pathlib import Path
from dotenv import load_dotenv
from disnake.ext import commands

#Logger
logging.basicConfig(format = "\033[1;32m{asctime} \033[1;37m| \033[1;34m{levelname} \033[1;37m| \033[1;31m{name}: \033[1;33m{message}", style = "{", datefmt = "%d-%m-%Y \033[1;37m| \033[1;32m%H:%M:%S", level = logging.INFO)

if BOT_TOKEN is None:
    logging.error("Missing Token.")
    exit()

#Bot Definition
intents = disnake.Intents.default()
intents.members = True
bot = commands.InteractionBot(intents = intents)

#Loading plugins
plugins = [file.stem for file in Path("plugins").glob("*.py")]
for extension in plugins:
    bot.load_extension(f"plugins.{extension}")
logging.info(f"Successfully Loaded Plugins: {', '.join(bot.cogs)}")

@bot.event
async def on_message(message):
    if isinstance(message.channel, disnake.DMChannel) and message.author != bot.user:
        logging.log(level = 100, msg = f"DM | {message.author}: {message.content}")

'''
Check if the account has been connected without using logging

@bot.event
async def on_ready():
    print(f"Successfully Logged As {bot.user}")

'''

bot.add_listener(errors.bot_error_handler, name = "on_slash_command_error")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)