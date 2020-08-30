from discord.ext import commands

from .permissions import PermissionManager
from config.config import dev_ids

def is_dev():
    async def check(ctx: commands.Context):
        return ctx.author.id in dev_ids

    return commands.check(check)

def permitted(level: int):
    async def check(ctx: commands.Context):
        roles = [role.name for role in ctx.author.roles]
        uid = str(ctx.author.id)

        valid = PermissionManager().has_perms(roles, uid, level)

        if valid:
            return True

        if not ctx.message.content.startswith("!help"):
            await ctx.send(f"You do not have the required permission level ({level}) required to run this command.", delete_after=15)
        return False

    return commands.check(check)