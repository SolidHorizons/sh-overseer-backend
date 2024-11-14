from Utils import Utils
import Constants
import difflib
from models.WordModel import WordModel

class ChatFilter:

    async def handleText(self, inputText : str) -> bool: 
        """
        Returns true or false if the text contains a word part of the wordlib.
        """
        deobfuscatedTextResult : str = await self.deobfuscateText(inputText)
        return await self.readTextForWordlib(deobfuscatedTextResult)

    
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
    

    async def readTextForWordlib(self, deobfuscatedText: str) -> list[str]:
        """
        Returns true or false based on if a word from wordlib is found.
        Fuzzy matching is used to find approximate matches.
        """
        wordlib : list[WordModel] = await Utils.fromJson(Constants.WORDLIBPATH, WordModel)

        words = [word.word for word in wordlib]

        exactMatches : list[str] = []
        fuzzyMatches : list[str] = []

        for wordToFilter in words:
            if deobfuscatedText.lower().__contains__(wordToFilter):
                exactMatches.append(wordToFilter)
        
        if len(exactMatches) > 0:
            print(f"exact finds: {exactMatches}")
            return exactMatches

        for wordInTextFuzzy in deobfuscatedText.lower().split(" "):
            fuzzyMatches : list[str] = difflib.get_close_matches(wordInTextFuzzy, words, n=Constants.WORDMAXFILTER, cutoff=Constants.FILTERCUTOFF)

        if len(fuzzyMatches) > 0:
            print(f"fuzzy finds: {fuzzyMatches}")
            return fuzzyMatches