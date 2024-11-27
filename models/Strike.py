from models.IModel import IModel
import Constants

class Strike(IModel):

    def __init__(self, strikeID : int, flagID : int, userStrikeCount : int):
        self.strikeID = strikeID
        self.flagID = flagID
        self.userStrikeCount = userStrikeCount


    @classmethod
    def from_dict(cls, data):
        return cls(
            strikeID=data["strikeID"],
            flaggedMessageID=data["flagID"],
            userStrikeCount=data["userStrikeCount"],
        )

    def to_dict(self):
        return {
            "strikeID" : self.strikeID,
            "flagID": self.flagID,
            "userStrikeCount": self.userStrikeCount,
        }