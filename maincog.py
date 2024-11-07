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

async def setup(bot: commands.Bot):
                                                                #SH ID
    await bot.add_cog(maincog(bot), guilds=[discord.Object(id=constants.SOLIDHORIZONSGUILDID)])

class maincog(commands.Cog):


    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self) -> None:       # when the cog is loaded in it will print in the console that it's working
        print(f'{self.__cog_name__} is ready')


    @commands.command()
    async def sync(self, ctx : discord.ext.commands.Context) -> None:
        print("in sync")
        bot : discord.ext.commands.Bot = ctx.bot
        fmt = await bot.tree.sync(guild=ctx.guild) 
        await ctx.send(f"synced {len(fmt)} commands")


    @app_commands.command(name="sayhello", description="say hello bot")
    async def sayhello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hello")
