import logging
import asyncio

from util.embeds import *
from disnake.ext import commands

logger = logging.getLogger(__name__)

async def bot_error_handler(inter, exception):
    if getattr(exception, "handled", False):
        #Errors already handled in cogs should have .handled = True
        return

    if isinstance(exception, commands.NotOwner):
        await inter.send(embed = embed_alert("Owner Only!"), ephemeral = True)
        await asyncio.sleep(5)
        await inter.delete_original_response()
    else:
        msg = "Ignoring exception in command {}: ".format(inter.application_command)
        exc_info = type(exception), exception, exception.__traceback__
        logger.exception(msg, exc_info = exc_info)