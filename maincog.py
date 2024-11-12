import discord
from discord.ext import commands
from discord import app_commands
import os
import logging as log
import datetime as dt
import asyncio
import json
import discord.ext.commands
import random
import math
import re
import discord.ext
import constants


async def setup(bot: commands.Bot) -> None:
    
    guilds : list[discord.Guild] = bot.guilds
    guildObjects : list[discord.Object] = []

    for guild in guilds:
        guildObjects.append(discord.Object(id=guild.id))
    
    await bot.add_cog(maincog(bot), guilds=guildObjects)


class maincog(commands.Cog):


    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self) -> None:       # when the cog is loaded in it will print in the console that it's working

        guilds : list[discord.Guild] = self.bot.guilds

        for guild in guilds:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild) 
            log.info(f"maincog in sync for {guild.name}")

        print(f'{self.__cog_name__} is ready')


    @app_commands.command(name="sayhello", description="say hello bot")
    async def sayhello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"hello {interaction.user.name}")
