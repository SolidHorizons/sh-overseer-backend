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
import aiohttp
import requests as rq

async def setup(bot: commands.Bot) -> None:
    
    await bot.add_cog(apicog(bot), guilds=[discord.Object(id=constants.SOLIDHORIZONSGUILDID)])

class apicog(commands.Cog):


    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self) -> None:       # when the cog is loaded in it will print in the console that it's working

        guilds : list[discord.Guild] = self.bot.guilds
        print(guilds)
        for guild in guilds:
            await self.bot.tree.sync(guild=guild) 
            print(f"in sync for {guild.name}")

        print(f'{self.__cog_name__} is ready')


    async def makeRequest(self, method, url, headers=None, params=None, data=None) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, headers=headers, params=params, data=data) as response:

                    log.info(f"Response status: {response.status}, URL: {url}, Params: {params}")

                    if response.content_type != 'application/json':
                        return {"status": "failed", "message": f"Unexpected response type: {response.content_type}"}
                    
                    if not await self.responseValidator(response.status):
                        return {"status" : "failed"}
                    
                    decodedResponse = await response.json()

                    if not await self.statusValidator(decodedResponse["status"]):
                        return {"status" : "failed"}
                    
                    return decodedResponse   
                  
        except json.JSONDecodeError as json_error:
            log.info(f"JSON Decode Error: {json_error}")
            return {"status" : "failed"}
        
        except rq.exceptions.InvalidJSONError as e:
            log.error(f"Request failed invalid JSON error: {e}")
            return {"status" : "failed"}
        
        except rq.exceptions.RequestException as e:
            log.error(f"Request failed: {e}")
            return {"status" : "failed"}
        
        except Exception as e:
            log.error(f"Exception encountered in makeRequest: {e}")
            return {"status" : "failed"}
        

    async def responseValidator(self, responseStatus : int) -> bool:
        try:
            log.info(responseStatus)
            if responseStatus == 200 or responseStatus == 201:
                return True
            else:
                return False
            
        except Exception as e:
            log.error(f"cant validate response: {e}")
            return False 
        
    
    async def statusValidator(self, responseStatus : dict) -> bool:
        try:
            if responseStatus == "success":
                return True
            else:
                return False
        except Exception as e:
            log.error(f"cant validate status: {e}")
            return False 