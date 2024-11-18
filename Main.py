import discord
from discord.ext import commands
import asyncio
import logging as log
import datetime as dt
import os
from dotenv import load_dotenv
import Constants
from Api import Api, startApi
from fastapi import FastAPI
import uvicorn
import threading

class main:

    def __init__(self):
        log_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        current_dir = os.path.dirname(__file__)
        log_file_path = os.path.join(current_dir, 'applogs', f'Log_{log_time}.txt')
        log.basicConfig(
            filename=log_file_path,
            level=log.INFO,
            format='[%(asctime)s] -- %(message)s',
            filemode='a'
        )
        log.raiseExceptions = False
        log.captureWarnings(False)

        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='*', intents=self.intents, application_id=Constants.APPLICATIONID)


    async def run_bot(self) -> None:
        await self.initiateCogs()
        await self.bot.start(Constants.DCKEY)  # start the bot


    async def initiateCogs(self):
        try:
            await self.bot.load_extension("MainCog")
        except Exception as e:
            print(f"Failed to load extensions: {e}")


    def run_api(self):
        api = startApi()  
        uvicorn.run(api, host="127.0.0.1", port=8000)


    def run_bot_loop(self) -> None:

        api_thread = threading.Thread(target=self.run_api, daemon=True)
        api_thread.start()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_bot())



if __name__ == "__main__":

    instMain = main()
    bot_thread = instMain.run_bot_loop()

