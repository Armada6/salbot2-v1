# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import language_check
from bot.utils.config_helper import ConfigHelper
from bot.utils.checks import permitted as requires

class Grammar(commands.Cog):
    """A cog that corrects grammar"""

    def __init__(self, bot):
        self.bot = bot
        self.enabled = False

    @commands.group(name="grammar")
    @requires(110)
    async def grammar(self, ctx: commands.Context):
        pass

    @grammar.command(name="enable")
    async def g_enable(self, ctx):
        self.enabled = True
        await ctx.channel.send("Enabled grammar checking.")

    @grammar.command(name="disable")
    async def g_disable(self, ctx):
        self.enabled = False
        await ctx.channel.send("Disabled grammar checking.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        content = message.content

        tool = language_check.LanguageTool("en-GB")

        matches = tool.check(content)
        if len(matches) == 0:
            return

        content = language_check.correct(content, matches)

        await message.channel.send(f"*\* {content}")

def setup(bot):
    bot.add_cog(Grammar(bot))
