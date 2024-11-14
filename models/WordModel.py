from models.IModel import IModel

class WordModel(IModel):

    def __init__(self, word, severity):       #creates an EventCycle object with serverdata, eventtype, what file needs to be swapped out and when it happened
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