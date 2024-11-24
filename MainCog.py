import discord
from discord.ext import commands
from discord import app_commands
import logging as log
import datetime as dt
import discord.ext
import Constants
from ChatFilter import ChatFilter


async def setup(bot: commands.Bot) -> None:
    
    guilds : list[discord.Guild] = bot.guilds
    guildObjects : list[discord.Object] = []

    for guild in guilds:
        guildObjects.append(discord.Object(id=guild.id))
    
    await bot.add_cog(maincog(bot), guilds=guildObjects)


class maincog(commands.Cog):


    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    instCF = ChatFilter()

    @commands.Cog.listener()
    async def on_ready(self) -> None:       # when the cog is loaded in it will print in the console that it's working

        guilds : list[discord.Guild] = self.bot.guilds

        for guild in guilds:
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild) 
            log.info(f"maincog in sync for {guild.name}")

        print(f'{self.__cog_name__} is ready')


    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):

        if message.content and Constants.ALLOWTEXTMODERATION:
            await self.instCF.handleText(context=message)

        if message.attachments and Constants.ALLOWOCR:
            await self.instCF.handleAttachments(message)

        if message.embeds and Constants.ALLOWOCR:
            await self.instCF.handleEmbed(message)


    @app_commands.command(name="sayhello", description="say hello bot")
    async def sayhello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"hello {interaction.user.name}")
