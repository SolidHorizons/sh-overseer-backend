from Utils import Utils
import Constants
import difflib
from models.WordModel import WordModel
from models.FlaggedMessage import FlaggedMessage
import discord

class ChatFilter:

    async def handleText(self, context : discord.Message) -> bool: 
        """
        Returns true or false if the text contains a word part of the wordlib.
        """
        deobfuscatedTextResult : str = await self.deobfuscateText(context.content)
        result : list[WordModel] | None = await self.readTextForWordlib(deobfuscatedTextResult)

        if result is None:

            return False
        
        highestSeverity = 0
        for wordMd in result:
            if wordMd.severity > highestSeverity:
                highestSeverity = wordMd.severity


        flaggedMessage = FlaggedMessage(context.guild.id, context.author.id, context.id, highestSeverity, [word.to_dict() for word in result])
        await Utils.appendToJson(Constants.FLAGGEDMESSAGESPATH, flaggedMessage)

        return True
        

    
    async def deobfuscateText(self, encodedText : str) -> str:
        """
        Returns a decoded string of the input text to match it into.
        """
        decodeDict = await Utils.fromJsonNoObject(Constants.DECODELIBPATH)
        result = []
        i = 0
        length = len(encodedText)

        while i < length:

            matched = False
            for j in range(5, 0, -1): 

                if i + j <= length and encodedText[i:i + j] in decodeDict:

                    result.append(decodeDict[encodedText[i:i + j]])
                    i += j
                    matched = True
                    break
            if not matched:

                result.append(encodedText[i])
                i += 1
                
        return ''.join(result)
    

    async def readTextForWordlib(self, deobfuscatedText: str) -> list[WordModel] | None:
        """
        Returns list of WordModel matches if a word (or multiple) from wordlib is found.
        """
        wordlib : list[WordModel] = await Utils.fromJson(Constants.WORDLIBPATH, WordModel) #loads in the word library

        exactMatches : list[WordModel] = []
        fuzzyResults : list[str] = []
        fuzzyMatches : list[WordModel] = []

        for wordMd in wordlib:
            if deobfuscatedText.lower().__contains__(wordMd.word): #checks text for exact matches
                exactMatches.append(wordMd)
        
            if len(exactMatches) > 0:
                return exactMatches

            for wordInTextFuzzy in deobfuscatedText.lower().split(" "):             #checks text for approximate matches
                fuzzyResults = difflib.get_close_matches(wordInTextFuzzy, wordMd.word, n=Constants.WORDMAXFILTER, cutoff=Constants.FILTERCUTOFF)
            
            if len(fuzzyResults) > 0:
                return None
            
            for result in fuzzyResults:
                for wordModel in wordlib:
                    if result == wordModel:
                        fuzzyMatches.append(wordModel)

            if len(fuzzyMatches) > 0:
                return fuzzyMatches
        
        return None