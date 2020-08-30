import discord
from discord.ext import commands

exempt_roles = ["Administrator", "Moderator", "SalC1 Bot", "SalC1 Bot - LP", "Dyno", "Dyno Premium", "BetterAntispam"]

async def punish_check(ctx: commands.Context, member: discord.Member):
    roles = [role.name for role in member.roles]
    for role in exempt_roles:
        if role in roles:
            await ctx.channel.send("You are not permitted to punish this member.")
            raise PermissionError()
    return True