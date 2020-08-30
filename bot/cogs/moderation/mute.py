import time
import discord
from discord.ext import commands, tasks
from discord.utils import get

from bot.bot import Bot
from bot.utils.checks import permitted
from .checks import punish_check, has_role, apply_role, remove_role


class Mute(commands.Cog):
    """Mute users"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="mute")
    @permitted(50)
    async def mute(self, ctx: commands.Context, member: discord.Member, time_hours: int = 24, *reason):
        await punish_check(ctx, member)
        if has_role(member, "Muted"):
            return await ctx.send("This user is already muted.")

        dm = True
        message = ""
        if "--no-dm" in reason:
            reason.remove("--no-dm")
            dm = False

        reason = " ".join(reason)
        await apply_role(ctx.guild, member, "Muted", reason)

        if dm:
            try:
                await member.send(f"You have been muted on the SalC1 Discord server for {time_hours} hours with the reason: `{reason}`")
            except:
                message = "(The user could not be DMed)"

        details = {
            "type": "mute",
            "name": str(member),
            "uid": str(member.id),
            "staff": str(ctx.author),
            "suid": str(ctx.author.id),
            "at": round(time.time()),
            "until": round(time.time() + time_hours * 3600),
            "guild": str(ctx.guild.id),
            "reason": reason
        }

        self.bot.api.insert("active_mutes", "mute_id", str(round(time.time() * 1000)), details)
        log_id = str(self.bot.api.size("modlogs"))
        self.bot.api.insert("modlogs", "log_id", log_id, details)

        mute_info = f"{ctx.author} muted member {member.mention} for {time_hours} hours with reason `{reason if reason else None}`, caseID: {log_id}. {message}"
        self.bot.logger.info(mute_info)
        await ctx.send(mute_info)

    @commands.command(name="unmute")
    @permitted(50)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *reason):
        if not has_role(member, "Muted"):
            return await ctx.send("This user isn't muted.")

        reason = " ".join(reason)
        await remove_role(ctx.guild, member, "Muted", reason)

        details = {
            "type": "unmute",
            "name": str(member),
            "uid": str(member.id),
            "staff": str(ctx.author),
            "suid": str(ctx.author.id),
            "at": round(time.time()),
            "guild": str(ctx.guild.id),
            "reason": reason
        }

        self.bot.api.delete("active_mutes", "uid", str(member.id))
        log_id = str(self.bot.api.size("modlogs"))
        self.bot.api.insert("modlogs", "log_id", log_id, details)

        mute_info = f"{ctx.author} unmuted member {member.mention} with reason `{reason if reason else None}`, caseID: {log_id}."
        self.bot.logger.info(mute_info)
        await ctx.send(mute_info)

    @commands.Cog.listener()
    async def on_ready(self):
        self.unmute_loop.start()

    @tasks.loop(seconds=15)
    async def unmute_loop(self):
        mutes = self.bot.api.get_all("active_mutes")

        for mute in mutes:
            if mute["until"] > round(time.time()):
                continue
            
            try:
                self.bot.api.delete("active_mutes", "mute_id", mute["mute_id"])
            except Exception as e:
                self.bot.logger.error(str(e))
            guild = get(self.bot.guilds, id=int(mute["guild"]))
            member = get(guild.members, id=int(mute["uid"]))

            try:
                await remove_role(guild, member, "Muted", "Automatic unmute. Time expired.")
            except Exception as e:
                self.bot.logger.error(str(e))
            else:
                self.bot.logger.info(f"Member {member} was unmuted automatically.")



def setup(bot: Bot):
    bot.add_cog(Mute(bot))