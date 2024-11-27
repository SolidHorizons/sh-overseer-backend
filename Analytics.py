from models.FlaggedMessage import FlaggedMessage
from models.Strike import Strike

class Analytics:

    async def getGuildStatistics(self, guildID : int) -> dict:
        """
        Returns all moderation statistics from a guild
        """
        GuildStats = {
            "bannedCount" : await self.getBannedCount(guildID),
            "flaggedCount" : await self.getFlaggedCount(guildID),
            "strikedCount" : await self.getStrikeCount(guildID)
        }
        return GuildStats


    async def getBannedCount(self, guildID : int) -> int:
        """
        Returns a total count of banned people from a guild
        """
        ...


    async def getFlaggedCount(self, guildID : int) -> int:
        """
        Returns a total count of flagged messages from a guild
        """
        ...


    async def getStrikeCount(self, guildID : int) -> int:
        """
        Returns a total count of strikes from a guild
        """
        ...


    async def getRecentFlagged(self, guildID : int, amount : int) -> list:
        """
        Returns a list of the latest flagged messages in a guild
        """
        ...


    async def getRecentBanned(self, guildID : int, amount : int) -> list:
        """
        Returns a list of the latest banned in a guild
        """
        ...


    async def getRecentStrikes(self, guildID : int, amount : int) -> list:
        """
        Returns a list of the latest strikes
        """
        ...