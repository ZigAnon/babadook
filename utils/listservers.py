#!/usr/bin/env python
# Author: TehZig#1949
import discord
import os

curDir = os.path.dirname(os.path.realpath(__file__))
config = open(curDir + "/../include/config")
lines = config.readlines()
TOKEN = lines[0].rstrip()
zigID = lines[1].rstrip()

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\nPress [Ctrl+C] to view servers\n')
    # to_leave = client.get_server(id)
    # await client.leave_server(to_leave)

client.run(TOKEN)

servers = list(client.servers)
print("\nConnected on " + str(len(client.servers)) + " servers:")
for x in range(len(servers)):
    print('  ' + servers[x-1].name + '\n    id: ' + servers[x-1].id)
