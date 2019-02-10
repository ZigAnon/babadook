#!/usr/bin/env python
# Author: TehZig#1949
import discord
import asyncio
import time
import os

curDir = os.path.dirname(os.path.realpath(__file__))
config = open(curDir + "/../include/config")
lines = config.readlines()
TOKEN = lines[0].rstrip()
zigID = lines[1].rstrip()
mainServ = lines[4].rstrip()
joinRole = lines[5].rstrip()
talkRole = lines[6].rstrip()
repRole = lines[35].rstrip()
userid = '334437537286193152'

client = discord.Client()

def is_political(m):
    with open(curDir + '/../include/polRoles') as p:
        political = [line.strip('\n').split(',') for line in p]
    for x in range(len(political)):
        role = discord.utils.get(m.server.roles, id = political[x-1][0])
        if role in m.roles:
            return True
    return False

def is_bot(m):
    if m.bot:
        return True
    else:
        return False

def is_mod(m):
    with open(curDir + '/../include/modRoles') as a:
        admin = [line.strip('\n').split(',') for line in a]
    for x in range(len(admin)):
        role = discord.utils.get(m.server.roles, id = admin[x-1][0])
        if role in m.roles:
            return True
    return False

def is_rep(m):
    rep = discord.utils.get(m.server.roles, id = repRole)
    if rep in m.roles:
        return True
    else:
        if is_mod(m):
            return True
    return False

def is_new(m):
    Snow2 = discord.utils.get(m.server.roles, id = joinRole)
    if Snow2 in m.roles:
        return True
    else:
        return False

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    server = client.get_server(mainServ)
    members = list(server.members)
    for x in range(len(members)):
        if not is_political(members[x-1]) and not is_bot(members[x-1]) and not is_rep(members[x-1]) and not is_new(members[x-1]):
            print('    ' + members[x-1].id + ' - ' + members[x-1].name)

    # member = server.get_member(userid)
    # Snow1 = discord.utils.get(server.roles, id = talkRole)
    # Snow2 = discord.utils.get(server.roles, id = joinRole)
    # await client.add_roles(member, Snow2)
    # await asyncio.sleep(1)
    # await client.remove_roles(member, Snow1)
    await client.close()

client.run(TOKEN)
