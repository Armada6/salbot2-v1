# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from bot.utils.config_helper import ConfigHelper

import re, io, aiohttp

badwords = ConfigHelper("./config/badwords.json").read()
badwords = list(map(re.compile, badwords))

def is_apng(a: bytes) -> bool:
    acTL = a.find(b"\x61\x63\x54\x4C")
    if acTL > 0:
        iDAT = a.find(b"\x49\x44\x41\x54")
        if acTL < iDAT:
            return True
    return False

async def message_contains_apng(message: discord.Message) -> bool:
    for embed in message.embeds:
        if embed.type == "image":
            async with aiohttp.ClientSession() as session:
                async with session.get(embed.url) as r:
                    try:
                        raw = await r.read()
                        if is_apng(raw):
                            return True
                    except Exception as e:
                        print(e)
                        return False

    for a in message.attachments:
        f = io.BytesIO()
        await a.save(f)
        if is_apng(f.read()):
            return True

    return False


class Content(commands.Cog):
    """Automatically remove malicious or inappropriate content"""

    def __init__(self, bot):
        self.bot = bot

    async def check(self, message: discord.Message):
        """Check a message for various content types that need to be removed"""

        if any(re.search(pattern, message.content.lower()) for pattern in badwords):
            await message.delete()
            await message.author.send("Please do not use inappropriate words in chat. Please report this to modmail if you think this warning was a mistake.")

        if await message_contains_apng(message):
            await message.delete()
            await message.channel.send("Due to abuse, the APNG image format is disabled here.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.check(after)


def setup(bot):
    bot.add_cog(Content(bot))