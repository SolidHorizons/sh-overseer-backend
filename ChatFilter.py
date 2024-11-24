from Utils import Utils
import Constants
import difflib
from models.WordModel import WordModel
from models.FlaggedMessage import FlaggedMessage
import discord
import logging as log
import cv2
from cv2 import typing
import pytesseract
import numpy as np
import time
import requests as rq
import json

class ChatFilter:

    async def handleText(self, context : discord.Message = None, text : str = None) -> bool: 
        """
        Returns true or false if the text contains a word part of the wordlib.
        """
        result : list[WordModel] = []

        if context:
            result = await self.readText(context.content)

        if text:
            result = await self.readText(text)

        if len(result) == 0:

            return False
        
        highestSeverity = 0
        for wordMd in result:
            if wordMd.severity > highestSeverity:
                highestSeverity = wordMd.severity

        await self.addFlaggedMessage(context, highestSeverity, result)

        return True
    

    async def readText(self, text) -> list[WordModel]:

        result : list[WordModel] = []

        deobfuscatedTextResult = await self.deobfuscateText(text)
        deobfuResultLower = deobfuscatedTextResult.lower()
        wordResults = await self.readTextForWordlib(deobfuResultLower)
        if wordResults:
            for word in wordResults:
                result.append(word)

        return result


    async def addFlaggedMessage(self, context : discord.Message, highestSeverity : int, result : list[WordModel]):
    
        flaggedMessages : list[FlaggedMessage] = await Utils.fromJson(Constants.FLAGGEDMESSAGESPATH, FlaggedMessage)

        try:
            flaggedIDMax = flaggedMessages[-1].flagID + 1
        except IndexError:
            log.info("index not available, setting ID 0")
        finally:
            flaggedIDMax = 0

        flaggedMessage = FlaggedMessage(flaggedIDMax, context.guild.id, context.author.id, context.id, highestSeverity, [word.to_dict() for word in result])
        await Utils.appendToJson(Constants.FLAGGEDMESSAGESPATH, flaggedMessage)



    async def handleEmbed(self, context : discord.Message) -> bool:
        """
        Returns true or false if the embed contains a word part of the wordlib.
        """
        for embed in context.embeds:
            textFromEmbed : str = await self.performOCR(embed.thumbnail.url)
            if textFromEmbed:
                await self.handleText(context=context, text=textFromEmbed.lower())
            

    async def handleAttachments(self, context : discord.Message) -> bool:
        """
        Returns true or false if the embed contains a word part of the wordlib.
        """
        for attachment in context.attachments:
            textFromEmbed : str = await self.performOCR(attachment.url)

            if textFromEmbed:
                await self.handleText(context=context, text=textFromEmbed)


    async def loadImageFromURL(self, url):
        """
        Load an image from a URL into an OpenCV format (ndarray).
        
        Args:
        url (str): The URL of the image.
        
        Returns:
        img (ndarray): The image in OpenCV format.
        """
        response = rq.get(url)
        imageArray = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(imageArray, cv2.IMREAD_COLOR) 
        return img

    
    async def preprocessImage(self, img : typing.MatLike):
        """
        Preprocess the image for OCR by resizing, converting to grayscale,
        applying GaussianBlur, and binarization.
        
        Args:
        img (ndarray): The input image in OpenCV format.
        
        Returns:
        processed_image (ndarray): The preprocessed image ready for OCR.
        """

        baseWidth : int = 800 
        wPercent : float = (baseWidth / float(img.shape[1]))
        hSize : int = int((float(img.shape[0]) * float(wPercent)))
        imgResized : typing.MatLike = cv2.resize(img, (baseWidth, hSize), interpolation=cv2.INTER_LINEAR)

        grayImg : typing.MatLike = cv2.cvtColor(imgResized, cv2.COLOR_BGR2GRAY)

        processedImg : typing.MatLike = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        return processedImg
    

    async def performOCR(self, imageUrl) -> str:
        """
        Process the image from URL and perform OCR to extract text.
        
        Args:
        image_url (str): The URL of the image.
        
        Returns:
        str: Extracted text from the image.
        """
        img : typing.MatLike = await self.loadImageFromURL(imageUrl)

        processedImage : typing.MatLike = await self.preprocessImage(img)
        text : str = pytesseract.image_to_string(processedImage)
        singleLine = ' '.join(text.split())

        return singleLine


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

            if deobfuscatedText.__contains__(wordMd.word): #checks text for exact matches
                exactMatches.append(wordMd)
        
            if len(exactMatches) > 0:
                print(exactMatches)
                return exactMatches

            for wordInTextFuzzy in deobfuscatedText.lower().split(" "):             #checks text for approximate matches
                fuzzyResults = difflib.get_close_matches(wordInTextFuzzy, wordMd.word, n=Constants.WORDMAXFILTER, cutoff=Constants.FILTERCUTOFF)
            
            for result in fuzzyResults:
                for wordModel in wordlib:
                    if result == wordModel:
                        fuzzyMatches.append(wordModel)

            if len(fuzzyMatches) > 0:
                return fuzzyMatches
        
        return None