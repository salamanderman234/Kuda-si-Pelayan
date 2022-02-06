import discord
from discord.ext import commands
import music
from asyncio import sleep
# from asyncio import sleep

cogs = [music]
activity = discord.Game(name="Youtube")
bot = commands.Bot(command_prefix='!',activity=activity, status=discord.Status.idle)
#untuk setup fitur
for i in cogs:
    i.setup(bot)


#untuk running bot
bot.run('OTM4MDAzNDM3NTI4OTU3MDE4.Yfj9xg.AoFMK2xoozHOHeax7dQSA37lmCY')
