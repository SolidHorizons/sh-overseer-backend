from models.IModel import IModel
from models.WordModel import WordModel
import Constants

class FlaggedMessage(IModel):

    def __init__(self, 
                 flagID : int,
                 guildID : int,
                 userID : int,
                 messageID : int,
                 severityFlag : Constants.SeverityFlag, 
                 triggeredWords : list[dict]
                ):
        
        self.flagID = flagID
        self.guildID = guildID
        self.userID = userID
        self.messageID = messageID
        self.severityFlag = severityFlag
        self.triggeredWords = triggeredWords


    @classmethod
    def from_dict(cls, data):
        return cls(
            flagID=data["flagID"],
            guildID=data["guildID"],
            userID=data["userID"],
            messageID = data["messageID"],
            severityFlag=data["severityFlag"],
            triggeredWords=data["triggeredWords"],
        )

    def to_dict(self):
        return {
            "flagID": self.flagID,
            "guildID": self.guildID,
            "userID": self.userID,
            "messageID": self.messageID,
            "severityFlag": self.severityFlag,
            "triggeredWords": self.triggeredWords,
        }