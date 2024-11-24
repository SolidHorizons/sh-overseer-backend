from models.IModel import IModel
from models.WordModel import WordModel
import Constants

class CustomWordLib(IModel):

    def __init__(self, libID : int, libName : str, wordContent : list[WordModel]):
        self.libID = libID
        self.libName = libName
        self.wordContent = wordContent


    @classmethod
    def from_dict(cls, data):
        return cls(
            libID=data["libID"],
            libName=data["libName"],
            wordContent=data["wordContent"],
        )

    def to_dict(self):
        return {
            "libID": self.libID,
            "libName": self.libName,
            "wordContent": self.wordContent
        }