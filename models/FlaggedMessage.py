from models.IModel import IModel
import Constants

class FlaggedMessage(IModel):

    def __init__(self, 
                 guildID : int,
                 userID : int,
                 severityFlag : Constants.SeverityFlag, 
                 flaggedMessages : list[str]
                ):
        
        self.guildID = guildID
        self.userID = userID
        self.severityFlag = severityFlag
        self.flaggedMessages = flaggedMessages


    @classmethod
    def from_dict(cls, data):
        return cls(
            guildID=data["guildID"],
            userID=data["userID"],
            severityFlag=data["severityFlag"],
            flaggedMessages=data["flaggedMessages"],
        )

    def to_dict(self):
        return {
            "guildID": self.guildID,
            "userID": self.userID,
            "severityFlag": self.severityFlag,
            "flaggedMessages": self.flaggedMessages,
        }