# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from bot.utils.config_helper import ConfigHelper
from bot.utils.checks import permitted as requires

class Faq(commands.Cog):
    """A cog that adds FAQ and other commands for SalC1 Bot"""

    def __init__(self, bot):
        self.bot = bot
        self.stats = ConfigHelper("./config/faqstats.json", {})
        self.faq_conf = ConfigHelper("./config/faq.json")

    def get_entry(self, items: list, entry: str):
        for item in items:
            if entry in item["names"]:
                return item
        return False

    def get_stats(self, itemname: str):
        data = self.stats.read()
        if not itemname in data:
            data[itemname] = 1
            return 1
        data[itemname] += 1
        return data[itemname]

    async def send_embed(self, ctx: commands.Context, title: str, description: str, colour, count: int):
        embed = discord.Embed(title=title, description=description, colour=colour)
        embed.set_footer(text=f"This command has been called {count} times | made by vcokltfre#6868")
        await ctx.send(embed=embed)

    @commands.command(name="faq")
    @requires(10)
    async def faq_cmd(self, ctx, item: str):
        faq = self.faq_conf.read()["faq"]

        entry = self.get_entry(faq, item)
        if entry:
            await self.send_embed(ctx, f"FAQ entry for {item}:", entry["content"], 0x4FFF4F, self.get_stats(entry["names"][0]))
            return
        await ctx.send(f"No FAQ entry was found for `{item.strip('@')}`")

    @commands.command(name="tos", aliases=["terms"])
    @requires(10)
    async def tos_cmd(self, ctx, item: str):
        tos = self.faq_conf.read()["tos"]

        entry = self.get_entry(tos, item)
        if entry:
            await self.send_embed(ctx, f"By agreeing to Discord's Terms of Service you agree not to:", entry["content"], 0xFF1F1F, self.get_stats(entry["names"][0]))
            return
        await ctx.send(f"No ToS entry was found for `{item.strip('@')}`")

    @commands.command(name="dgl", aliases=["guidelines"])
    @requires(10)
    async def dgl_cmd(self, ctx, item: str):
        dgl = self.faq_conf.read()["dgl"]

        entry = self.get_entry(dgl, item)
        if entry:
            await self.send_embed(ctx, f"Discord guidelines entry for {item}:", entry["content"], 0xFF1F1F, self.get_stats(entry["names"][0]))
            return
        await ctx.send(f"No guidelines entry was found for `{item.strip('@')}`")


def setup(bot):
    bot.add_cog(Faq(bot))
