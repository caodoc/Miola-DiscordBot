import time
import asyncio

from util.embeds import *
from disnake.ext import commands

class Default(commands.Cog, description = "Bot's default commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = "Everyone - Check my ping.")
    async def ping(self, inter):
        start = time.perf_counter()
        await inter.response.send_message(":ping_pong: Pong!")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await inter.edit_original_message(content = f"REST API latency: {int(duration)}ms\n" f"Gateway API latency: {int(self.bot.latency * 1000)}ms")

    @commands.slash_command(description = "Owner - Send DMs.")
    @commands.is_owner()
    async def dm(self, inter, user_id: str, msg: str):
        user = await self.bot.fetch_user(user_id)

        if user is None:
            await inter.response.send_message("Can't find user.", ephemeral = True)
        else:
            channel = await self.bot.create_dm(user)
            await channel.send(msg)
            await inter.response.send_message("Message sent successfully.", ephemeral = True)

    @commands.slash_command(description = "Owner - Send message on the current channel.")
    @commands.is_owner()
    async def say(self, inter, msg: str):
        await inter.channel.send(msg)
        await inter.response.send_message("Message sent successfully.", ephemeral = True)
        await asyncio.sleep(1)
        await inter.delete_original_response()

    @commands.slash_command(description = "Everyone - About the creator")
    async def creator(self, inter):
        await inter.response.send_message("## Creator: Ducca \n ## Discord: caodoc \n ## Github: [Ducca](https://github.com/caodoc)")

    @commands.slash_command(description = "Owner - Servers list.")
    @commands.is_owner()
    async def serverlist(self, inter):
        #Replies with info on the bot's guilds
        await inter.response.defer()

        guilds = [f"{guild.name} own by {guild.owner.name}" for guild in self.bot.guilds]
        guilds.sort(key = lambda x: (x[1]))

        content = f"## I\'m in {len(guilds)} server!\n{guilds}"
        await inter.send(content)

def setup(bot):
    bot.add_cog(Default(bot))