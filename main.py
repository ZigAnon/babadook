# Author: TehZig#1949
# Work with Python 3.6
import discord
import asyncio
import os

timeout = 60*120  # 120 minutes
role_id = '506479342537146368'
rmRole = '506261279921668136'  # I'm New Here Role
addRole = '506264946418384907'  # Not a Lurker Role

curDir = os.path.dirname(os.path.realpath(__file__))
config = open(curDir + "/config")
lines = config.readlines()
TOKEN = lines[0].rstrip()
zigID = lines[1].rstrip()

############################
# Code to be added
############################

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('.iam') and (discord.utils.get(message.author.roles, id = addRole) is None):
        rmrole = discord.utils.get(message.server.roles, id = rmRole)
        addrole = discord.utils.get(message.server.roles, id = addRole)
        await client.add_roles(message.author, addrole)
        await asyncio.sleep(1)
        await client.remove_roles(message.author, rmrole)

############################
# Code to be added
############################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
