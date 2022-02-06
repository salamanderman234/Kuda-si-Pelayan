import discord
from discord.ext import commands
import dotenv
import os
import music
from asyncio import sleep
# from asyncio import sleep


token = os.getenv("BOT_TOKEN")
cogs = [music]
activity = discord.Game(name="Youtube")
bot = commands.Bot(command_prefix='!',activity=activity, status=discord.Status.idle)
#untuk setup fitur
for i in cogs:
    i.setup(bot)


#untuk running bot
bot.run(token)
