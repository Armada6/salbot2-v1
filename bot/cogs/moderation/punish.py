import time
import discord
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import permitted
from .checks import punish_check

appeals_server = None


class Punish(commands.Cog):
    """Punishments such as bans, kick, and warns"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="ban")
    @permitted(50)
    async def ban(self, ctx: commands.Context, member: discord.Member, *reason):
        await punish_check(ctx, member)
        reason = list(reason)

        dm = True
        appeal = ""
        message = ""
        if "--no-dm" in reason:
            reason.remove("--no-dm")
            dm = False
        if "--no-appeal" in reason:
            reason.remove("--no-appeal")
            appeal = f" You can appeal this decision by messaging modmail in this server: {appeals_server}"
        reason = " ".join(reason)

        if dm:
            try:
                await member.send(f"You have been banned the SalC1 Discord server with the reason: `{reason}`.{appeal}")
            except:
                message = "(The user could not be DMed)"

        try:
            await member.ban(reason=reason)
        except Exception as e:
            self.bot.logger.error(str(e))
            return await ctx.channel.send("Banning the user failed.")

        details = {
            "type": "ban",
            "name": str(member),
            "uid": str(member.id),
            "staff": str(ctx.author),
            "suid": str(ctx.author.id),
            "at": round(time.time()),
            "guild": str(ctx.guild.id),
            "reason": reason
        }

        log_id = str(self.bot.api.size("modlogs"))
        self.bot.api.insert("modlogs", "log_id", log_id, details)

        ban_info = f"{ctx.author} banned member {member.mention} with reason `{reason if reason else None}`, caseID: {log_id}. {message}"
        self.bot.logger.info(ban_info)
        await ctx.send(ban_info)

    @commands.command(name="warn")
    @permitted(50)
    async def warn(self, ctx: commands.Context, member: discord.Member, *reason):
        await punish_check(ctx, member)
        reason = list(reason)

        dm = True
        escalate = False
        message = ""
        if "--no-dm" in reason:
            reason.remove("--no-dm")
            dm = False
        if "--escalate" in reason:
            reason.remove("--escalate")
            escalate = True
        reason = " ".join(reason)

        if dm:
            try:
                await member.send(f"You have been warned on the SalC1 Discord server with the reason: `{reason}`.")
            except:
                if escalate:
                    await ctx.channel.send("Escalating to mute as the user couldn't be DMed.")
                    mess = ctx.message
                    ct = mess.content.replace("!warn", "!mute")
                    ct = ct.replace("--escalate", "")
                    mess.content = ct
                    print(mess.content)
                    return await self.bot.process_commands(mess)
                message = "(The user could not be DMed)"

        details = {
            "type": "warn",
            "name": str(member),
            "uid": str(member.id),
            "staff": str(ctx.author),
            "suid": str(ctx.author.id),
            "at": round(time.time()),
            "guild": str(ctx.guild.id),
            "reason": reason
        }

        log_id = str(self.bot.api.size("modlogs"))
        self.bot.api.insert("modlogs", "log_id", log_id, details)

        warn_info = f"{ctx.author} warned member {member.mention} with reason `{reason if reason else None}`, caseID: {log_id}. {message}"
        self.bot.logger.info(warn_info)
        await ctx.send(warn_info)


def setup(bot: Bot):
    bot.add_cog(Punish(bot))