import discord
from discord.ext import commands
from discord.utils import get

exempt_roles = ["Administrator", "Moderator", "SalC1 Bot", "SalC1 Bot - LP", "Dyno", "Dyno Premium", "BetterAntispam"]

async def punish_check(ctx: commands.Context, member: discord.Member):
    roles = [role.name for role in member.roles]
    for role in exempt_roles:
        if role in roles:
            await ctx.channel.send("You are not permitted to punish this member.")
            raise PermissionError()
    return True

async def apply_role(guild: discord.Guild, member: discord.Member, role: str, reason: str = "No reason given"):
    role = get(guild.roles, name=role)
    await member.add_roles(role, reason=reason)

async def remove_role(guild: discord.Guild, member: discord.Member, role: str, reason: str = "No reason given"):
    role = get(guild.roles, name=role)
    await member.remove_roles(role, reason=reason)

def has_role(member: discord.Member, role: str):
    return role in [role.name for role in member.roles]