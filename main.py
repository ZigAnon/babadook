#!/usr/local/bin/python3.6
# Author: TehZig#1949
import discord
from discord.ext import commands
import asyncio
import os

timeout = 60*120  # 120 minutes
role_id = '506479342537146368'
rmRole = '506261279921668136'  # I'm New Here Role
addRole = '506264946418384907'  # Not a Lurker Role

curDir = os.path.dirname(os.path.realpath(__file__))
config = open(curDir + "/include/config")
lines = config.readlines()
TOKEN = lines[0].rstrip()
zigID = lines[1].rstrip()

############################
# Code to be added
############################

zdesc = '''Thanks for using ZigBot!'''

bot = commands.Bot(command_prefix='zb!', description=zdesc)

@bot.event
async def on_message(message):
    if message.content.startswith('.iam') and (discord.utils.get(message.author.roles, id = addRole) is None):
        rmrole = discord.utils.get(message.server.roles, id = rmRole)
        addrole = discord.utils.get(message.server.roles, id = addRole)
        await bot.add_roles(message.author, addrole)
        await asyncio.sleep(1)
        await bot.remove_roles(message.author, rmrole)
    else:
        # Needed per FAQ
        # https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
        await bot.process_commands(message)

############################
# Code to be added
############################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
