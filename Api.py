from fastapi import FastAPI, HTTPException
from Utils import Utils
import Constants

class Api:

    def __init__(self) -> None:
        self.app = FastAPI()
        self.setupRoutes()


    def setupRoutes(self) -> None:
        """
        initialises the api routes of the bot and routes them to the correct functions
        """

        @self.app.get("/")
        async def api_root():
            return await self.APIRoot()
        
        @self.app.get("/wordlib/")
        async def api_wordlib():
            return await self.APIWordlib()
        

    async def APIRoot(self) -> dict:
        """
        root of api
        """
        return {"message": "Hello World."}
    

    async def APIWordlib(self) -> dict:
        """
        returns the wordlibrary
        """
        return {"message": await Utils.fromJsonNoObject(Constants.WORDLIBPATH)}
        
            
def startApi() -> FastAPI:
    api_instance = Api()
    return api_instance.app 