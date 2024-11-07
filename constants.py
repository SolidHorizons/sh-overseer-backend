import datetime as dt
import os
from dotenv import load_dotenv


#functions reuired to set a constant
load_dotenv()


#constants from .env
APPLICATIONID = os.getenv("applicationID")
BETAAPPLICATIONID = os.getenv("betaApplicationID")
DCKEY = os.getenv("dcKey")
BETADCKEY = os.getenv("betaDcKey")


#constants relating to discord
SOLIDHORIZONSGUILDID = 1259185634334081084