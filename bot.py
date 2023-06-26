import disnake
import logging

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
intents.message_content = True
intents.members = True
bot = commands.InteractionBot(intents = intents)

#Loading plugins
plugins = [file.stem for file in Path("plugins").glob("*.py")]
for extension in plugins:
    bot.load_extension(f"plugins.{extension}")
logging.info(f"Successfully Loaded Plugins: {', '.join(bot.cogs)}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if isinstance(message.channel, disnake.DMChannel):
        logging.log(level = 100, msg = f"DM - {message.author}: {message.content}")
    else:
        logging.log(level = 100, msg = f"{message.channel} - {message.author}: {message.content}")

    if message.content.startswith("hello"):
        await message.channel.send(f"Hello from the other side of the screen, {message.author}!")

    if message.content.startswith("ily"):
        await message.channel.send(f"ily too {message.author} <3")

'''
Check if the account has been connected without using logging

@bot.event
async def on_ready():
    print(f"Successfully Logged As {bot.user}")

'''

bot.add_listener(errors.bot_error_handler, name = "on_slash_command_error")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)