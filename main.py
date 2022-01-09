import discord

from discord.ext import commands

from config_loader import load_config

TOKEN = load_config().get("token")
PREFIX = load_config().get("prefix")
STATUS = load_config().get("activity_status")

BOT = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), case_insensitive=True)


@BOT.event
async def on_ready():
    """ When bot connected and ready to work. """
    BOT.load_extension("cogs.send_online")
    print("send_online cog was loaded ")

    activity = discord.Game(name=STATUS)
    await BOT.change_presence(status=discord.Status.online, activity=activity)
    print("Bot successfully connected")


if __name__ == "__main__":
    BOT.run(TOKEN)
