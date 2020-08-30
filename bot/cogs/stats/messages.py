import time
import discord
from discord.ext import commands

from bot.bot import Bot


class Messages(commands.Cog):
    """Message activity tracking for SalC1 Bot"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        uid = str(message.author.id)
        user = self.bot.api.get_by_uid("messages", "user_id", uid)
        if not user:
            data = {
                "creation": round(time.time()),
                "messages": 1
            }
            self.bot.api.insert("messages", "user_id", uid, data)
        else:
            self.bot.api.update("messages", "user_id", uid, {"messages": user["messages"] + 1})


def setup(bot: Bot):
    bot.add_cog(Messages(bot))