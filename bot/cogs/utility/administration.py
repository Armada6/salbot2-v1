# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from bot.utils.checks import permitted as requires
from bot.utils.permissions import PermissionManager

usage = "Usage: `!perms <'grant'|'edit'|'remove'> <'user'|'role'> <user|role> [level]`"


class Administration(commands.Cog):
    """Administration commands for SalC1 Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="perms", aliases=["permissions"])
    @requires(1000)
    async def perms_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send(usage)

    @perms_group.command(name="grant", aliases=["edit"])
    async def perms_grant(self, ctx: commands.Context, permission_type: str, operand: str, level: int):
        """Grant a permission level to a user or role"""
        if permission_type == "user":
            PermissionManager().add_override(operand, level)
            await ctx.channel.send(f"Set permission level for user {operand} to {level}")
        elif permission_type == "role":
            PermissionManager().add_role(operand, level)
            await ctx.channel.send(f"Set permission level for role {operand} to {level}")
        else:
            await ctx.channel.send(usage)

    @perms_group.command(name="remove")
    async def perms_remove(self, ctx: commands.Context, permission_type: str, operand: str):
        """Remove a permission override for a user or role"""
        if permission_type == "user":
            PermissionManager().del_override(operand)
            await ctx.channel.send(f"Removed permission override for user {operand}")
        elif permission_type == "role":
            PermissionManager().add_role(operand)
            await ctx.channel.send(f"Removed permission override for role {operand}")
        else:
            await ctx.channel.send(usage)

    @commands.command(name="ping")
    @requires(10)
    async def ping(self, ctx: commands.Context):
        """Get the Discord API ping"""
        await ctx.channel.send(f"> Pong! {round(self.bot.latency * 1000)}ms")

    @commands.group(name="slowmode")
    @requires(75)
    async def slowmode(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send("Usage: `!slowmode <'set'|'remove'> [time (s)]`")

    @slowmode.command(name="set")
    async def sm_set(self, ctx: commands.Context, sm_time: int, channel: discord.TextChannel = None):
        """Set the slowmode delay for a channel"""
        channel = channel if channel else ctx.channel
        await channel.edit(slowmode_delay=sm_time)
        await ctx.channel.send(f"Set slowmode for {channel} to {sm_time}s")

    @slowmode.command(name="remove")
    async def sm_remove(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Remove slowmode for a channel"""
        channel = channel if channel else ctx.channel
        await channel.edit(slowmode_delay=0)
        await ctx.channel.send(f"Removed slowmode for {channel}")

    @commands.command(name="nick")
    @requires(25)
    async def nickname(self, ctx: commands.Context, *name):
        name = " ".join(name)
        await ctx.author.edit(nick=name)


def setup(bot):
    bot.add_cog(Administration(bot))
