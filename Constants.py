import datetime as dt
import os
from dotenv import load_dotenv
from enum import Enum


#functions reuired to set a constant
load_dotenv()


#constants from .env
APPLICATIONID = os.getenv("applicationID")
BETAAPPLICATIONID = os.getenv("betaApplicationID")
DCKEY = os.getenv("dcKey")
BETADCKEY = os.getenv("betaDcKey")


#data paths
WORDLIBPATH = os.path.join(os.path.dirname(__file__), "data", "wordlib.json")
DECODELIBPATH = os.path.join(os.path.dirname(__file__), "data", "decodelib.json")
FLAGGEDMESSAGESPATH = os.path.join(os.path.dirname(__file__), "data", "flaggedmessages.json")


#Chat filter constants
WORDMAXFILTER = 2
FILTERCUTOFF = 0.4


#enums
class SeverityFlag(Enum):
    ACTION_NONE = 0
    ACTION_MILD = 1
    ACTION_SEVERE = 2
    ACTION_EXTREME = 3