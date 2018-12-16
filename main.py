#!/usr/local/bin/python3.6
# Author: TehZig#1949
# v0.4
import discord
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from random import randint
import asyncio
import os

timeout = 60*5  # 5 minutes
dateFormat = '%Y-%m-%d %H:%M:%S.%f'

curDir = os.path.dirname(os.path.realpath(__file__))

# Your config file may not need all these conditions
# I find it helps keep the code clean
config = open(curDir + "/include/config")
lines = config.readlines()
TOKEN = lines[0].rstrip()
zigID = lines[1].rstrip()
testChan = lines[2].rstrip()
testServ = lines[3].rstrip()
mainServ = lines[4].rstrip()
joinRole = lines[5].rstrip()
talkRole = lines[6].rstrip()
muteRole = lines[7].rstrip()
jailRole = lines[8].rstrip()
shetRole = lines[9].rstrip()
config.close()

brain = open(curDir + "/include/brainlet")
brainlet = brain.readlines()
brain.close()

fun = open(curDir + "/include/eastereggs")
funEggs = fun.readlines()
fun.close()

fun = open(curDir + "/include/easterlinks")
funLinks = fun.readlines()
fun.close()

# Assigns role to add and remove
try:
    r = open(curDir + '/logs/db/' + mainServ + '.roles')
    newRoles = r.readlines()
    servMod = newRoles[0].rstrip() # Moderator
    servRep = newRoles[1].rstrip() # Representative
except:
    pass
r.close()

zdesc = '''Thanks for using ZigBot!'''
bot = commands.Bot(command_prefix='.', description=zdesc)

############################
############################

# Main loop, do not comment this area out
async def main_loop():
    await bot.wait_until_ready()

############################
############################

    channel = discord.Object(id=testChan)
    servers = list(bot.servers)
    pinged = [0] * len(servers)
    timeoff = 0
    count = 0
    
    # Checks each server for disboard bump
    # Uses existing data to remind if needed
    while not bot.is_closed:
        # Needed vars
        curTime = datetime.now()

        for x in range(len(servers)):
            filePath = curDir + '/logs/db/' + str(servers[x-1].id)

            # Looks for time file
            try:
                t = open(filePath + '.time')
                tStrip = t.readlines()
                oldTime = tStrip[0].rstrip()
                found = 1
                t.close()
            except:
                found = 0

            # If time file exists
            if found:
                if pinged[x-1] == 0:
                    lastBump = datetime.strptime(oldTime, dateFormat)
                    c = open(filePath + '.channel')
                    cStrip = c.readlines()
                    bumChan = cStrip[0].rstrip()
                    c.close()
                    channel = discord.Object(id=bumChan)

                    # Check Time
                    if lastBump < curTime:
                        pinged[x-1] = 1
                        lastBump += timedelta(hours=1)

                        # Ping all Admins
                        if lastBump < curTime:
                            await bot.send_message(channel, '@here, helps us grow: ' + '\n Please \`!disboard bump\` again!')

                        # Ping member only
                        else:
                            m = open(filePath + '.member')
                            mStrip = m.readlines()
                            bumMemb = mStrip[0].rstrip()
                            m.close()
                            pMemb = '<@' + bumMemb + '>'
                            await bot.send_message(channel, '%s Friendly reminder to \`!disboard bump\` again!' % pMemb)

                # Has it been an hour since last ping?
                else:
                    try:
                        l = open(filePath + '.lping')
                        lStrip = l.readlines()
                        lPing = lStrip[0].rstrip()
                        lastPing = datetime.strptime(lPing, dateFormat) + timedelta(hours=1) - timedelta(minutes=2)
                    except:
                        l = open(filePath + '.lping', 'w+')
                        l.write("%s\r\n" % (curTime))
                        lastPing = curTime + timedelta(hours=1) - timedelta(minutes=2)
                    l.close()

                    # Resets ping timer
                    if lastPing < curTime:
                        pinged[x-1] = 0
                        os.remove(filePath + '.lping')

            '''if found is 1 and count > 4:
                count = 0
                members = list(servers[x-1].members)
                memNum = 0
                for i in range(len(members)):
                    rolNum = 0
                    roles = list(members[i-1].roles)
                    for j in range(len(roles)):
                        rolNum += 1
                    if rolNum is 2:
                        # set roles
                        member = members[i-1]
                        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
                        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
                        await bot.add_roles(member, Snow2)
                        await asyncio.sleep(1)
                        await bot.remove_roles(member, Snow1)
                        timeoff += 1
                    rolNum = 0'''

        # checks again in one min
        # count += 1
        reboot = 60 - timeoff
        await asyncio.sleep(reboot) # task runs every 60 seconds less mx time

# Need to add scanner on server join to issue punishments
# This will prevent leaving and rejoining to remove punishment
@bot.command(pass_context = True, description = "Removes all write permissions from all channels.")
async def mute(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        mute = discord.utils.get(member.server.roles, id = muteRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        await bot.say(embed=embed)
        await bot.add_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes mute status.")
async def unmute(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        mute = discord.utils.get(member.server.roles, id = muteRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User unmuted.", description="**{0}** follow the rules.".format(member, ctx.message.author), color=0x27d300)
        await bot.say(embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes all chats and allows user to state case in jail chat.")
async def jail(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        jail = discord.utils.get(member.server.roles, id = jailRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User Jailed!", description="**{0}** was jailed by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        await bot.say(embed=embed)
        await bot.add_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Frees member from jail")
async def free(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        jail = discord.utils.get(member.server.roles, id = jailRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User Freed!", description="**{0}** was freed by **{1}**!".format(member, ctx.message.author), color=0x27d300)
        await bot.say(embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Banishes member to shitpost chat.")
async def shitpost(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        shit = discord.utils.get(member.server.roles, id = shetRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="Shitposter!", description="**{0}** was given Shitposter by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        channel = discord.Object(id='509243584143425537')
        msg = '<@' + member.id + '>'
        await bot.send_message(channel, 'Looks like you pushed it too far ' + msg + '. You live here now. Enjoy!!')
        await bot.say(embed=embed)
        await bot.add_roles(member, shit)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes shitpost tag.")
async def cleanpost(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        shit = discord.utils.get(member.server.roles, id = shetRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="Good Job!", description="**{0}** it seems **{1}** has faith in you.".format(member, ctx.message.author), color=0x27d300)
        await bot.say(embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, shit)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

############################
############################

@bot.event
async def on_message(message):
    # Stops bot from replying to self
    if message.author == bot.user:
        return

############################
############################

    if ' iq' in message.content.lower() or 'iq ' in message.content.lower():
        msg = await bot.send_message(message.channel, message.author.mention + ', there are better arguments than IQ to make your case.\nhttps://www.independent.co.uk/news/science/iq-tests-are-fundamentally-flawed-and-using-them-alone-to-measure-intelligence-is-a-fallacy-study-8425911.html\nhttps://www.cell.com/neuron/fulltext/S0896-6273(12)00584-3')
        await asyncio.sleep(timeout)
        await bot.delete_message(msg)

    if 'smart' in message.content.lower():
        x = randint(0,5)
        brainletURL = brainlet[x].rstrip()
        msg = await bot.send_message(message.channel, 'I is r b smartr den u.\n' + brainletURL)
        await asyncio.sleep(5)
        await bot.delete_message(msg)

    for x in range(len(funEggs)):
        eEgg = funEggs[x-1].rstrip()
        if eEgg in message.content.lower():
            y = (x-1) * 2
            z = y+1
            phrase = funLinks[y].rstrip()
            phraseURL = funLinks[z].rstrip()
            msg = await bot.send_message(message.channel, message.author.mention + ' ' + phrase + '\n' + phraseURL)
            await asyncio.sleep(8)
            await bot.delete_message(msg)

    if message.content.startswith('!disboard bump'):
        # Needed vars
        bumServ = message.server.id
        bumChan = message.channel.id
        bumMemb = message.author.id
        channel = discord.Object(id=bumChan)
        curTime = datetime.now()
        newTime = datetime.now() + timedelta(hours=2)
        filePath = curDir + '/logs/db/' + bumServ
 
        # Replaces member and channel
        # Old info not needed only updated
        oldMemb = open(filePath + '.member', 'w+')
        oldMemb.write("%s\r\n" % (bumMemb))
        oldMemb.close()
        oldChan = open(filePath + '.channel', 'w+')
        oldChan.write("%s\r\n" % (bumChan))
        oldChan.close()

        # Loads existing needed time data
        # If not found, creates data
        try:
            t = open(filePath + '.time')
            tStrip = t.readlines()
            oldTime = tStrip[0].rstrip()
        except:
            t = open(filePath + '.time', 'w+')
            t.write("%s\r\n" % (str(newTime)))
            oldTime = str(newTime)
        t.close()

        lastBump = datetime.strptime(oldTime, dateFormat)

        # Tests if 2 hours has passed
        # If not, it lets you know it'll remind you later
        # It always updates member and channel
        if curTime < lastBump:
            diff = int(int((lastBump - curTime).seconds)/60) + 1
            await bot.send_message(channel, 'I\'ll remind you to bump here in ' + str(diff) + ' minutes.')
        else:
            await bot.send_message(channel, 'I\'ll remind you in 120 mins to bump disboard again.')
            t = open(filePath + '.time', 'w+')
            t.write("%s\r\n" % (str(newTime)))
            t.close()

    if message.content.startswith('.iam'):
        if discord.utils.get(message.author.roles, id = talkRole) is None and discord.utils.get(message.author.roles, id = joinRole) is not None:
            Snow1 = discord.utils.get(message.server.roles, id = talkRole)
            Snow2 = discord.utils.get(message.server.roles, id = joinRole)
            await bot.add_roles(message.author, Snow1)
            print('Snow1 add is: ' + str(Snow1))
            await asyncio.sleep(1)
            await bot.remove_roles(message.author, Snow2)
            print('Snow2 remove is: ' + str(Snow2))

############################
############################

    # If no on_message command invoked, check bot commands
    else:
        # https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
        await bot.process_commands(message)

############################
############################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    servers = list(bot.servers)
    for x in range(len(servers)):
        print("    " + servers[x-1].id + " - " + servers[x-1].name + " (Members: " + str(len(servers[x-1].members)) + ")")

bot.loop.create_task(main_loop())
bot.run(TOKEN)
