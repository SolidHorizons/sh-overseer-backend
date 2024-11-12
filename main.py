import discord
from discord.ext import commands
import asyncio
import logging as log
import datetime as dt
import os
from dotenv import load_dotenv
import constants


class main:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'applogs', f'Log_{log_time}.txt')
        log.basicConfig(
            filename=log_file_path,
            level=log.INFO,
            format=f'[%(asctime)s] -- %(message)s',
            filemode='a'
        )
        log.raiseExceptions = False
        log.captureWarnings(False)


    intents = discord.Intents.all()                            #"applicationID" / "betaApplicationID"
    bot = commands.Bot(command_prefix='*', intents=intents, application_id=constants.APPLICATIONID)


    def run_bot_loop(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_bot())


    async def run_bot(self) -> None:

        await self.initiateCogs() #"dcKey" / "betaDcKey"
        await self.bot.start(constants.DCKEY) # start the bot


    async def initiateCogs(self):
        try:
            await self.bot.load_extension("maincog")
            await self.bot.load_extension("apicog")

        except Exception as e:
            print(f"Failed to load extensions: {e}")



if __name__ == "__main__":

    instMain = main()
    bot_thread = instMain.run_bot_loop()

