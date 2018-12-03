#!/usr/local/bin/python3.6
# Author: TehZig#1949
# v0.4
import discord
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
import asyncio
import os

timeout = 60*120  # 120 minutes
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
oldServ = lines[4].rstrip()
mainServ = lines[5].rstrip()
config.close()

try:
    r = open(curDir + '/logs/db/' + oldServ + '.roles')
    oldRoles = r.readlines()
    rmRole = oldRoles[0].rstrip() # I'm New Here Role
    addRole = oldRoles[1].rstrip() # Not a Lurker Role
except:
    pass
r.close()

zdesc = '''Thanks for using ZigBot!'''
bot = commands.Bot(command_prefix='.', description=zdesc)

############################
############################

async def main_loop():
    await bot.wait_until_ready()

############################
############################

    channel = discord.Object(id=testChan)
    servers = list(bot.servers)
    pinged = [0] * len(servers)
    
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

        # checks again in one min
        await asyncio.sleep(60) # task runs every 60 seconds

# Need to add scanner on server join to issue punishments
# This will prevent leaving and rejoining to remove punishment
@bot.command(pass_context = True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        mute = discord.utils.get(member.server.roles, id = '517140313408536576')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.add_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        mute = discord.utils.get(member.server.roles, id = '517140313408536576')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="User unmuted.", description="**{0}** follow the rules.".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True)
async def jail(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        jail = discord.utils.get(member.server.roles, id = '509865275705917440')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="User Jailed!", description="**{0}** was jailed by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.add_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True)
async def free(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        jail = discord.utils.get(member.server.roles, id = '509865275705917440')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="User Freed!", description="**{0}** was freed by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True)
async def shitpost(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        shit = discord.utils.get(member.server.roles, id = '509865272283496449')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="Shitposter!", description="**{0}** was given Shitposter by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
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

@bot.command(pass_context = True)
async def cleanpost(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator and ctx.message.server.id == mainServ:
        shit = discord.utils.get(member.server.roles, id = '509865272283496449')
        Snow1 = discord.utils.get(member.server.roles, id = '513156267024449556')
        Snow2 = discord.utils.get(member.server.roles, id = '517850437626363925')
        embed=discord.Embed(title="Good Job!", description="**{0}** it seems **{1}** has faith in you.".format(member, ctx.message.author), color=0xff00f6)
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

    if 'iq' in message.content.lower() and message.server.id == mainServ:
        await bot.send_message(message.channel, message.author.mention + ', there are better arguments than IQ to make your case.\nhttps://www.independent.co.uk/news/science/iq-tests-are-fundamentally-flawed-and-using-them-alone-to-measure-intelligence-is-a-fallacy-study-8425911.html\nhttps://www.cell.com/neuron/fulltext/S0896-6273(12)00584-3')

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
        if discord.utils.get(message.author.roles, id = addRole) is None and (message.server.id == oldServ):
            rmrole = discord.utils.get(message.server.roles, id = rmRole)
            addrole = discord.utils.get(message.server.roles, id = addRole)
            await bot.add_roles(message.author, addrole)
            await asyncio.sleep(1)
            await bot.remove_roles(message.author, rmrole)
        if (message.server.id == mainServ) and discord.utils.get(message.author.roles, id = '513156267024449556') is None and discord.utils.get(message.author.roles, id = '517140313408536576') is None and discord.utils.get(message.author.roles, id = '509865272283496449') is None and discord.utils.get(message.author.roles, id = '509865275705917440') is None:
            Snow1 = discord.utils.get(message.server.roles, id = '513156267024449556')
            Snow2 = discord.utils.get(message.server.roles, id = '517850437626363925')
            await bot.add_roles(message.author, Snow1)
            await asyncio.sleep(1)
            await bot.remove_roles(message.author, Snow2)

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
