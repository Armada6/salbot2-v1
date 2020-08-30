from bot.bot import run

run([
    "bot.cogs.utility.general",
    "bot.cogs.moderation.mute",
    "bot.cogs.moderation.punish"
], True)