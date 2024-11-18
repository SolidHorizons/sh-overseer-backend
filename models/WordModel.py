from models.IModel import IModel
import Constants

class WordModel(IModel):

    def __init__(self, word : str, severity : Constants.SeverityFlag):
        self.word = word
        self.severity = severity


    @classmethod
    def from_dict(cls, data):
        return cls(
            word=data["word"],
            severity=data["severity"],
        )

    def to_dict(self):
        return {
            "word": self.word,
            "severity": self.severity,
        }