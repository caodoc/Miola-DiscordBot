import asyncio
import logging

from constants import *
from disnake.ext import commands

root_logger = logging.getLogger()
logger = logging.getLogger(__name__)

class Logging(commands.Cog, logging.Handler):
    def __init__(self, bot, owner_id):
        logging.Handler.__init__(self)
        self.bot = bot
        self.owner_id = owner_id
        self.queue = asyncio.Queue()
        self.task = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_ready(self):
        self.task = asyncio.create_task(self._log_task())
        username = f"{self.bot.user.name}#{self.bot.user.discriminator}"
        msg = f"Successfully Logged As {username}"
        self.logger.info(msg)

    async def _log_task(self):
        while True:
            record = await self.queue.get()
            owner = await self.bot.fetch_user(self.owner_id)
            if owner is not None:
                try:
                    msg = self.format(record)
                    await owner.send(f"{msg}")
                except:
                    self.handleError(record)

    # logging.Handler overrides below.

    def emit(self, record):
        self.queue.put_nowait(record)

    def close(self):
        if self.task:
            self.task.cancel()

def setup(bot):
    if OWNER_ID is None:
        logger.warning("Skipping installation of logging cog as owner ID is not provided.")
        return

    logging_cog = Logging(bot, int(OWNER_ID))
    logging_cog.setLevel(logging.WARNING)
    logging_cog.setFormatter(logging.Formatter(fmt = "{asctime} | {levelname} | {name}: {message}", style = "{", datefmt = "%d-%m-%Y | %H:%M:%S"))
    root_logger.addHandler(logging_cog)
    bot.add_cog(logging_cog)