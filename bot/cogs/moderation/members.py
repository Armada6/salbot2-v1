# -*- coding: utf-8 -*-

from discord.ext import commands
from discord.utils import get
import discord
from bot.utils.checks import permitted as requires

class Members(commands.Cog):
    """A member management cog for SalC1 Bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addmember")
    @requires(30)
    async def add_member(self, ctx: commands.Context, member: discord.Member):
        """Allows anyone with the permission level 30 or higher to give someone the 'Member' role"""
        member_role = get(member.guild.roles, name="Member")
        await member.add_roles(member_role)
        await ctx.channel.send(f"{ctx.author} has given the member role to {member}")

    @commands.command(name="removemember")
    @requires(30)
    async def remove_member(self, ctx: commands.Context, member: discord.Member):
        """Allows anyone with the permission level 30 or higher to remove the 'Member' role from someone"""
        member_role = get(member.guild.roles, name="Member")
        await member.remove_roles(member_role)
        await ctx.channel.send(f"{ctx.author} has removed the member role from {member}")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        roles = [role.name for role in after.roles]
        has_yt = "YouTube Member" in roles
        has_sp = "YouTube Sponsor" in roles

        if has_yt and not has_sp:
            role = after.guild.get_role(674163197694967818)
            await after.add_roles(role, reason="Autosponsor")


def setup(bot):
    bot.add_cog(Members(bot))
