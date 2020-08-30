# -*- coding: utf-8 -*-

from bot.utils.checks import permitted as requires
from discord.ext import commands
from discord.utils import get
import discord
from bot.utils.config_helper import ConfigHelper

class Reactions(commands.Cog):
    """Automatically give a user a role if they react to a message"""

    def __init__(self, bot):
        self.bot = bot
        self.cfg = ConfigHelper("./config/reactions.json")
        self.data = self.cfg.read()
        self.guild, self.role = None, None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(int(self.data["guild_id"]))
        self.role = self.guild.get_role(self.data["role_id"])

    def blacklist(self, uid: int):
        data = self.cfg.read()
        if uid in data["blacklist"]:
            return
        data["blacklist"].append(uid)
        self.cfg.write(data)

    def unblacklist(self, uid: int):
        data = self.cfg.read()
        if not uid in data["blacklist"]:
            return
        data["blacklist"].pop(data["blacklist"].index(uid))
        self.cfg.write(data)

    def is_relevant_reaction(self, emoji_object):
        id_ = None
        if isinstance(emoji_object, discord.PartialEmoji):
            id_ = emoji_object.id
        if isinstance(emoji_object, discord.Reaction):
            id_ = emoji_object.emoji.id
        return id_ == self.data["emoji_id"]

    async def add_role(self, member: discord.Member):
        await member.add_roles(self.role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.data["message_id"]:
            return
        if payload.user_id in self.data["blacklist"]:
            return
        if self.is_relevant_reaction(payload.emoji):
            member = get(self.guild.members, id=payload.user_id)
            await self.add_role(member)

    @commands.group(name="pack")
    @requires(50)
    async def pack_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send("Usage: `!pack <'mute'|'unmute'> <user_id>`")

    @pack_group.command(name="mute")
    async def pack_mute(self, ctx: commands.Context, member: int):
        self.blacklist(member)
        await ctx.channel.send(f"Pack: muted {member}")

    @pack_group.command(name="unmute")
    async def pack_unmute(self, ctx: commands.Context, member: int):
        self.unblacklist(member)
        await ctx.channel.send(f"Pack: unmuted {member}")


def setup(bot):
    bot.add_cog(Reactions(bot))
