import os
import traceback

import discord
from discord.ext import commands

from modules.counter import scheduler
from utils.essentials import functions
from utils.essentials.functions import func

config = functions.get("utils/config.json")
bot = commands.Bot(command_prefix=config.prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    cogs = 0
    for file in os.listdir("modules/cogs"):
        if file.endswith(".py"):
            cogs += 1
    print(f'Loaded {cogs} Cogs\nLogged in as: {bot.user.name}\nAPI Version: {discord.__version__}\n\n')

    try:
        guild = bot.get_guild(540784184470274069)
        people = format(len(guild.members), ",")
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {people} people"))
    except Exception as e:
        pass
    await scheduler(bot)


func.progress()
for file in os.listdir("modules"):
    if file.endswith(".py"):
        name = file[:-3]
        try:
            bot.load_extension(f"modules.{name}")
        except Exception as error:
            traceback.print_exc()

bot.load_extension("utils.essentials.errorhandler")
bot.run(config.token, reconnect=True)
