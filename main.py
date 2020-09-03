from bot.bot import run

run([
    "bot.cogs.utility.general",
    "bot.cogs.utility.administration",
    "bot.cogs.utility.faq",
    "bot.cogs.moderation.mute",
    "bot.cogs.moderation.content",
    "bot.cogs.moderation.members",
    "bot.cogs.moderation.punish",
    "bot.cogs.moderation.reactions",
    "bot.cogs.stats.messages",
    "bot.cogs.utility.grammar",
    #"bot.cogs.stats.presence",
    "jishaku"
], False)