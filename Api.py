from fastapi import FastAPI, HTTPException

class Api:

     
    def __init__(self):
        self.app = FastAPI()
        self.setup_routes()


    def setup_routes(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Hello World."}
        
            
def startApi() -> FastAPI:
    api_instance = Api()
    return api_instance.app 