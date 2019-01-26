#!/usr/local/bin/python3.6
# Author: TehZig#1949
# Use at your own risk.
# This bot was used with multiple servers and then coded for single
# Much of this bot is now server specific 'github' is more for archive
# I may rewrite it some day to work for multiple servers again
# v0.5
import discord
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from random import randint
from time import sleep
import asyncio
import json
import os
import requests

timeout = 60*5  # 5 minutes
dateFormat = '%Y-%m-%d %H:%M:%S.%f'
newAccount = 72 # 48 hours

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
logAct = lines[10].rstrip()
adminChan = lines[11].rstrip()
ox_id = lines[12].rstrip()
ox_key = lines[13].rstrip()
web_id = lines[14].rstrip()
web_key = lines[15].rstrip()
welcomeChan = lines[16].rstrip()
adminLogs = lines[17].rstrip()
oldRole = lines[18].rstrip()
seriousRole = lines[19].rstrip()
botChan = lines[20].rstrip()
ruleChan = lines[21].rstrip()
genChan = lines[22].rstrip()
shetChan = lines[23].rstrip()
newsChan = lines[24].rstrip()
nsfwChan = lines[25].rstrip()
offtChan = lines[26].rstrip()
botRole = lines[27].rstrip()
busyRole = lines[28].rstrip()
voiceChan = lines[29].rstrip()
gen2Chan = lines[30].rstrip()
cheetiID = lines[31].rstrip()
config.close()

jR = open(curDir + "/include/jailRoles")
lines = jR.readlines()
memeRoles = map(str.strip, lines)
memeRoles = ['.iam ' + x for x in memeRoles]
jR.close()

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
bot.remove_command("help")

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

        # Auto purge channels
        beforeTime = datetime.now() - timedelta(hours=12)
        oldNews = datetime.now() - timedelta(days=5)
        try:
            channel = discord.Object(id=botChan)
            await bot.purge_from(channel, limit=100, before=beforeTime)
        except:
            pass
        try:
            sChannel = discord.Object(id=shetChan)
            await bot.purge_from(sChannel, limit=100, before=oldNews)
        except:
            pass
        try:
            nChannel = discord.Object(id=newsChan)
            await bot.purge_from(nChannel, limit=100, before=oldNews)
        except:
            pass
        try:
            gChannel = discord.Object(id=genChan)
            await bot.purge_from(gChannel, limit=100, before=beforeTime, check=is_bot)
        except:
            pass
        try:
            g2Channel = discord.Object(id=gen2Chan)
            await bot.purge_from(g2Channel, limit=100, before=beforeTime, check=is_bot)
        except:
            pass
        try:
            oChannel = discord.Object(id=offtChan)
            await bot.purge_from(oChannel, limit=100, before=beforeTime, check=is_bot)
        except:
            pass
        try:
            nsChannel = discord.Object(id=nsfwChan)
            await bot.purge_from(nsChannel, limit=100, before=beforeTime, check=is_text)
        except:
            pass

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
                            await bot.send_message(channel, '@here, helps us grow: ' + '\n Please `!disboard bump` again!')

                        # Ping member only
                        else:
                            m = open(filePath + '.member')
                            mStrip = m.readlines()
                            bumMemb = mStrip[0].rstrip()
                            m.close()
                            pMemb = '<@' + bumMemb + '>'
                            await bot.send_message(channel, '%s Friendly reminder to `!disboard bump` again!' % pMemb)

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
        # count += 1
        reboot = 60 - timeoff
        await asyncio.sleep(reboot) # task runs every 60 seconds less mx time


############################
############################

#   Start of functions     #

############################
############################

def is_zig(m):
    if int(m.author.id) == int(zigID):
        return True
    else:
        return False

def is_cheeti(m):
    if int(m.author.id) == int(cheetiID):
        return True
    else:
        return False

def is_bot(m):
    if m.author.bot:
        return True
    else:
        return False

def is_text(m):
    if 'http' in m.content.lower():
        return False
    try:
        url = str(m.attachments[0]['url'])
        return False
    except:
        return True

def is_legacy(m):
    N = 30 # number of days before serious role
    oldmember = datetime.now() - timedelta(days=N)
    if m.author.joined_at < oldmember:
        Snow1 = discord.utils.get(m.author.server.roles, id = talkRole)
        if Snow1 in m.author.roles:
            return True
    return False

def is_in_trouble(m):
    try:
        filePath = curDir + '/logs/db/' + str(member.id)

        # Looks for punish file
        t = open(filePath + '.punish')
        t.close()
        return True
    except:
        return False

def num_roles(m):
    x = len(list(m.author.roles))
    return x

############################
############################

#   Start of Bot Commands  #

############################
############################

@bot.command(pass_context = True, description = "Posts hot chicks")
async def hotchicks(ctx):
    await bot.delete_message(ctx.message)
    msg = await bot.say('**All these hot chicks**\nhttps://media.giphy.com/media/madDH4fTGefvvL8P96/giphy.gif')
    await asyncio.sleep(30)
    await bot.delete_message(msg)

@bot.command(pass_context = True, description = "Redirects to roles page")
async def roles(ctx):
    await bot.delete_message(ctx.message)
    roleChan = bot.get_channel('512473259376246808')
    msg = await bot.say('You can view roles by typing `.lsar` or going to ' + roleChan.mention)
    await asyncio.sleep(15)
    await bot.delete_message(msg)

@bot.command(pass_context = True, description = "Defines word using Oxford Living Dictionary.")
async def define(ctx):
    raw = ctx.message.clean_content.lower()
    curTime = datetime.now()
    endTime = curTime + timedelta(seconds=10)
    word_id = raw.split('.define ')[1]
    word_id = word_id.replace(' ', '_')
    language = 'en'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'  + language + '/'  + word_id.lower()
    linkurl = '<https://' + language + '.oxforddictionaries.com/definition/' + word_id + '>'

    #url Normalized frequency
    urlFR = 'https://od-api.oxforddictionaries.com:443/api/v1/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
    r = requests.get(url, headers = {'app_id' : ox_id, 'app_key' : ox_key})

    # Checks for 404 or if Definitions is found
    if r.status_code is 200:
        # Builds the list to reduce API calls
        try:
            data = r.json()
            howmany = list(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'])
            exit = False
        except:
            howmany = [None]
            exit = True

        # Skips if error
        if exit is False:
            word_str = word_id.replace('_', ' ')
            defNumb = 0
            change = 1
            addReact = 1
            first = True
            firstSet = True
            forward = 'right'
            step = 'left'

            # Checks for definition change, if none, it stops
            while True:
                if change is 1:
                    change = 0
                    embed=discord.Embed(title="Oxford Living Dictionary:", url='https://' + language + '.oxforddictionaries.com/definition/' + word_id, color=0xf5d28a)
                    oxford = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][defNumb]['definitions']
                    embed.add_field(name=word_str.capitalize() + ':', value=oxford[0], inline=False)
                    embed.set_footer(text=str(defNumb+1) + ' of ' + str(len(howmany)))
                    if addReact is 0:
                        await bot.edit_message(msg, embed=embed)

                if addReact is 1:
                    addReact = 0
                    msg = await bot.say(embed=embed)
                    l = await bot.add_reaction(msg, '\U00002B05')
                    m = await bot.add_reaction(msg, '\U000027A1')
                    nav = None
                else:
                    nav = await bot.wait_for_reaction(timeout=1, emoji=['\U00002B05','\U000027A1'], message=msg)
                    if first:
                        first = False
                        nav = None

                    if nav and firstSet:
                        firstSet = False
                        forward = nav.reaction
                        step = nav.reaction
                    elif nav:
                        step = nav.reaction


                    if forward is step:
                        endTime = curTime + timedelta(seconds=10)
                        nav = None
                        step = None
                        change = 1
                        if defNumb < len(howmany)-1:
                            defNumb += 1
                    elif step:
                        endTime = curTime + timedelta(seconds=10)
                        nav = None
                        step = None
                        change = 1
                        if defNumb > 0:
                            defNumb -= 1
                    else:
                        pass

                    # time check
                    # if time is > 10 secs
                    # exit = True

                curTime = datetime.now()
                if curTime > endTime:
                    exit = True

                if exit is True or len(howmany) is 1:
                    break
            await bot.clear_reactions(msg)

    else:
        word_id = word_id.replace('_', ' ')
        msg = await bot.say('Unable to find **' + word_id.capitalize() + '** in Oxford Living')
        await asyncio.sleep(15)
        await bot.delete_message(msg)

@bot.command(pass_context = True, description = "Defines word using Merriam-Webster Dictionary.")
async def wdefine(ctx):
    raw = ctx.message.clean_content.lower()
    curTime = datetime.now()
    endTime = curTime + timedelta(seconds=10)
    word_id = raw.split('.wdefine ')[1]
    word_id = word_id.replace(' ', '_')
    language = 'en'
    url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' + word_id.lower() + '?key=' + web_key
    linkurl = '<https://www.merriam-webster.com/dictionary/' + word_id.lower() + '>'

    #url Normalized frequency
    r = requests.get(url)

    # Checks for 404 or if Definitions is found
    if r.status_code is 200:
        # Builds the list to reduce API calls
        try:
            data = r.json()
            howmany = len(list(data))
            exit = False
        except:
            howmany = [None]
            exit = True

        # Skips if error
        if exit is False:
            word_str = word_id.replace('_', ' ')
            defNumb = 0
            change = 1
            addReact = 1
            first = True
            firstSet = True
            forward = 'right'
            step = 'left'

            # Checks for definition change, if none, it stops
            while True:
                if change is 1:
                    change = 0
                    embed=discord.Embed(title="Merriam-Webster Dictionary:", url='https://www.merriam-webster.com/dictionary/' + word_id.lower(), color=0xf5d28a)
                    try:
                        webster = data[defNumb]['shortdef']
                    except:
                        word_id = word_id.replace('_', ' ')
                        msg = await bot.say('Unable to find **' + word_id.capitalize() + '** in Merriam-Webster')
                        await asyncio.sleep(15)
                        await bot.delete_message(msg)
                        break
                    embed.add_field(name=word_str.capitalize() + ':', value=webster[0], inline=False)
                    embed.set_footer(text=str(defNumb+1) + ' of ' + str(howmany))
                    if addReact is 0:
                        await bot.edit_message(msg, embed=embed)

                if addReact is 1:
                    addReact = 0
                    msg = await bot.say(embed=embed)
                    l = await bot.add_reaction(msg, '\U00002B05')
                    m = await bot.add_reaction(msg, '\U000027A1')
                    nav = None
                else:
                    nav = await bot.wait_for_reaction(timeout=1, emoji=['\U00002B05','\U000027A1'], message=msg)
                    if first:
                        first = False
                        nav = None

                    if nav and firstSet:
                        firstSet = False
                        forward = nav.reaction
                        step = nav.reaction
                    elif nav:
                        step = nav.reaction


                    if forward is step:
                        endTime = curTime + timedelta(seconds=10)
                        nav = None
                        step = None
                        change = 1
                        if defNumb < howmany-1:
                            defNumb += 1
                    elif step:
                        endTime = curTime + timedelta(seconds=10)
                        nav = None
                        step = None
                        change = 1
                        if defNumb > 0:
                            defNumb -= 1
                    else:
                        pass

                    # time check
                    # if time is > 10 secs
                    # exit = True

                curTime = datetime.now()
                if curTime > endTime:
                    exit = True

                if exit is True or howmany is 1:
                    break
            await bot.clear_reactions(msg)

@bot.command(pass_context = True, description = "Removes all write permissions from all channels.")
async def mute(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        mute = discord.utils.get(member.server.roles, id = muteRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        old = discord.utils.get(member.server.roles, id = oldRole)
        serious = discord.utils.get(member.server.roles, id = seriousRole)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
        await asyncio.sleep(1)
        await bot.remove_roles(member, old)
        await asyncio.sleep(1)
        await bot.remove_roles(member, serious)

        # punishment evasion
        p = open(filePath + '.punish', 'w+')
        p.close()

        # Kick from voice channel
        kick_channel = await bot.create_channel(ctx.message.server, "kick", type=discord.ChannelType.voice)
        await bot.move_member(member, kick_channel)
        await bot.delete_channel(kick_channel)
                    
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes mute status.")
async def unmute(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        mute = discord.utils.get(member.server.roles, id = muteRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User unmuted.", description="**{0}** follow the rules.".format(member, ctx.message.author), color=0x27d300)
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, mute)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)

        # Clear punishment
        try:
            os.remove(filePath + '.punish')
        except:
            pass
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes all chats and allows user to state case in jail chat.")
async def jail(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        jail = discord.utils.get(member.server.roles, id = jailRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        old = discord.utils.get(member.server.roles, id = oldRole)
        serious = discord.utils.get(member.server.roles, id = seriousRole)
        embed=discord.Embed(title="User Jailed!", description="**{0}** was jailed by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
        await asyncio.sleep(1)
        await bot.remove_roles(member, old)
        await asyncio.sleep(1)
        await bot.remove_roles(member, serious)

        # punishment evasion
        p = open(filePath + '.punish', 'w+')
        p.close()

        # Kick from voice channel
        kick_channel = await bot.create_channel(ctx.message.server, "kick", type=discord.ChannelType.voice)
        await bot.move_member(member, kick_channel)
        await bot.delete_channel(kick_channel)
 
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Frees member from jail")
async def free(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        jail = discord.utils.get(member.server.roles, id = jailRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User Freed!", description="**{0}** was freed by **{1}**!".format(member, ctx.message.author), color=0x27d300)
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)

        # Clear punishment
        try:
            os.remove(filePath + '.punish')
        except:
            pass

#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Banishes member to shitpost chat.")
async def shitpost(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        shit = discord.utils.get(member.server.roles, id = shetRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        old = discord.utils.get(member.server.roles, id = oldRole)
        serious = discord.utils.get(member.server.roles, id = seriousRole)
        embed=discord.Embed(title="Shitposter!", description="**{0}** was given Shitposter by **{1}**!".format(member, ctx.message.author), color=0xd30000)
        channel = discord.Object(id='533390486845653027')
        msg = '<@' + member.id + '>'
        await bot.send_message(channel, 'Looks like you pushed it too far ' + msg + '. You live here now. Enjoy!!')
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, shit)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
        await asyncio.sleep(1)
        await bot.remove_roles(member, old)
        await asyncio.sleep(1)
        await bot.remove_roles(member, serious)

        # punishment evasion
        p = open(filePath + '.punish', 'w+')
        p.close()

        # Kick from voice channel
        kick_channel = await bot.create_channel(ctx.message.server, "kick", type=discord.ChannelType.voice)
        await bot.move_member(member, kick_channel)
        await bot.delete_channel(kick_channel)
 
#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

@bot.command(pass_context = True, description = "Removes shitpost tag.")
async def cleanpost(ctx, member: discord.Member):
    if (ctx.message.author.server_permissions.administrator or discord.utils.get(ctx.message.author.roles, id=servMod) or discord.utils.get(ctx.message.author.roles, id=servRep)) and ctx.message.server.id == mainServ:
        filePath = curDir + '/logs/db/' + member.id
        shit = discord.utils.get(member.server.roles, id = shetRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="Good Job!", description="**{0}** it seems **{1}** has faith in you.".format(member, ctx.message.author), color=0x27d300)
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, shit)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)

        # Clear punishment
        try:
            os.remove(filePath + '.punish')
        except:
            pass

#    else:
        # embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        # await bot.say(embed=embed)

############################
############################

@bot.event
async def on_voice_state_update(before,after):
    with open(curDir + '/include/voice') as v:
        voiceID = [line.strip('\n').split(',') for line in v]
    if after.voice.voice_channel is not None:
        for x in range(len(voiceID)):
            if int(after.voice.voice_channel.id) == int(voiceID[x-1][0]):
                see = discord.utils.get(after.server.roles, id = voiceID[x-1][1])
                await bot.add_roles(after, see)
                break
    if before.voice.voice_channel is not None:
        await asyncio.sleep(1)
        for x in range(len(voiceID)):
            if int(before.voice.voice_channel.id) == int(voiceID[x-1][0]):
                hide = discord.utils.get(after.server.roles, id = voiceID[x-1][1])
                await bot.remove_roles(after, hide)
                break

############################
############################

############################
############################

@bot.event
async def on_message(message):
    # Stops bot from replying to self
    if message.author == bot.user or message.author.bot:
        return

############################
############################
    if is_legacy(message) and not is_in_trouble(message):
        serious = discord.utils.get(message.author.server.roles, id = seriousRole)
        await bot.add_roles(message.author, serious)

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

    # Eastereggs - disabled 181221 due to distracting
    '''for x in range(len(funEggs)):
        eEgg = funEggs[x-1].rstrip()
        if eEgg in message.content.lower():
            y = (x-1) * 2
            z = y+1
            phrase = funLinks[y].rstrip()
            phraseURL = funLinks[z].rstrip()
            msg = await bot.send_message(message.channel, message.author.mention + ' ' + phrase + '\n' + phraseURL)
            await asyncio.sleep(8)
            await bot.delete_message(msg)'''

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

    # allow disboard bump stop
    if message.content.startswith('!disboard stop') and message.author.server_permissions.administrator:
        disboard = discord.utils.get(message.server.members, name='DISBOARD')
        bumServ = message.server.id
        bumChan = message.channel.id
        filePath = curDir + '/logs/db/' + bumServ
        channel = discord.Object(id=bumChan)
        msg = await bot.wait_for_message(timeout=3, author=disboard)
        try:
            os.remove(filePath + '.time')
            await bot.delete_message(msg)
            await bot.send_message(channel, 'I\'ll stop reminding you for now. `!disboard bump` to start again.')
        except:
            await bot.send_message(channel, 'I\'m already set to not remind you. Please `!disboard bump` to start again.')

    if message.content.lower().startswith('.iam busy') and message.author.server.id == mainServ:
        if message.author.server_permissions.administrator:
            msg = await bot.send_message(message.channel,'As much as I would like to, I\'m not able to set you to busy.\n It\'s out of my power.')
            await bot.delete_message(message)
            await asyncio.sleep(10)
            await bot.delete_message(msg)
            return

        error = discord.utils.get(message.server.members, name='ZigBot')
        msg = await bot.wait_for_message(timeout=3, author=error)
        await bot.delete_message(msg)
        filePath = curDir + '/logs/db/' + message.author.id
        roles_busy = list(message.author.roles)
        with open(filePath + '.busy', 'w+') as f:
            for x in range(len(roles_busy)):
                f.write('%s\n' % roles_busy[x-1].id)
                await bot.remove_roles(message.author, roles_busy[x-1])
                await asyncio.sleep(1)
        addRole = discord.utils.get(message.server.roles, id = busyRole)
        await bot.add_roles(message.author, addRole)
        await bot.delete_message(message)
        return

    if message.content.lower().startswith('.iamn busy') and message.author.server.id == mainServ:
        error = discord.utils.get(message.server.members, name='ZigBot')
        msg = await bot.wait_for_message(timeout=3, author=error)
        await bot.delete_message(msg)
        filePath = curDir + '/logs/db/' + message.author.id
        with open(filePath + '.busy') as f:
            roles_active = [line.strip('\n') for line in f]
        for x in range(len(roles_active)):
            addRole = discord.utils.get(message.server.roles, id = str(roles_active[x-1]))
            await bot.add_roles(message.author, addRole)
            await asyncio.sleep(1)
        rmRole = discord.utils.get(message.server.roles, id = busyRole)
        await bot.remove_roles(message.author, rmRole)

        try:
            os.remove(filePath + '.busy')
        except:
            pass
        await bot.delete_message(message)
        return
    
    if message.content.lower().startswith('.iam'):
        if message.content.lower().startswith('.iamz') and is_zig(message):
            zigBot = discord.utils.get(message.server.roles, id = botRole)
            if not zigBot in message.author.roles:
                msg = await bot.send_message(message.channel,'You\'re the boss')
                await bot.add_roles(message.author, zigBot)
                await bot.delete_message(message)
                await asyncio.sleep(10)
                await bot.delete_message(msg)
            else:
                msg = await bot.send_message(message.channel,'Until you need me again.')
                await bot.remove_roles(message.author, zigBot)
                await bot.delete_message(message)
                await asyncio.sleep(10)
                await bot.delete_message(msg)
            return
        elif message.content.lower().startswith('.iamz'):
            await bot.send_message(message.channel, message.author.mention + ' You\'re not Zig.')
            return
        if message.content.lower().startswith('.iam epic') and is_cheeti(message):
            zigBot = discord.utils.get(message.server.roles, id = botRole)
            if not zigBot in message.author.roles:
                msg = await bot.send_message(message.channel,'You\'re epic!')
            #     await bot.add_roles(message.author, zigBot)
                await asyncio.sleep(timeout)
                await bot.delete_message(msg)
                await bot.delete_message(message)
            else:
                msg = await bot.send_message(message.channel,'You\'re epic!')
            #     await bot.remove_roles(message.author, zigBot)
                await asyncio.sleep(timeout)
                await bot.delete_message(msg)
                await bot.delete_message(message)
            return
        elif message.content.lower().startswith('.iam epic'):
            await bot.send_message(message.channel, message.author.mention + ' You\'re not epic.')
            return
        Snow1 = discord.utils.get(message.server.roles, id = talkRole)
        Snow2 = discord.utils.get(message.server.roles, id = joinRole)
        # Checks for single role or if user removed all roles
        await asyncio.sleep(1)
        if message.content.lower().startswith('.iamn') and discord.utils.get(message.author.roles, id = busyRole) is None:
            await asyncio.sleep(1)
            if num_roles(message) is 2:
                # User removed role, revert
                msg = await bot.send_message(message.channel, 'You aren\'t allowed to chat without an ideology.  Please choose a role from #roles or `.lsar`')
                await bot.add_roles(message.author, Snow2)
                await asyncio.sleep(1)
                await bot.remove_roles(message.author, Snow1)
                await asyncio.sleep(7)
                await bot.delete_message(msg)
                await bot.delete_message(message)

        # Checks for initial role to remove undecided
        elif discord.utils.get(message.author.roles, id = talkRole) is None and discord.utils.get(message.author.roles, id = joinRole) is not None and num_roles(message) > 2:
            await bot.add_roles(message.author, Snow1)
            await asyncio.sleep(1)
            await bot.remove_roles(message.author, Snow2)

        # If role doesn't exist
        elif num_roles(message) == 2:
            if discord.utils.get(message.author.roles, id = busyRole) is None:
                msg = await bot.send_message(message.channel, 'Please choose a role from #roles or `.lsar`')
            else:
                msg = await bot.send_message(message.channel, 'Your status is still set to busy.\n Please `.iamn busy` to get your roles back.')
            await asyncio.sleep(7)
            await bot.delete_message(msg)
            await bot.delete_message(message)

        # Checks for meme roles to shitpost
        message.content = message.content.lower()
        for x in range(len(memeRoles)):
            if message.content.startswith(memeRoles[x-1]):
                filePath = curDir + '/logs/db/' + message.author.id
                shit = discord.utils.get(message.server.roles, id = shetRole)
                Snow1 = discord.utils.get(message.server.roles, id = talkRole)
                Snow2 = discord.utils.get(message.server.roles, id = joinRole)
                channel = discord.Object(id='533390486845653027')
                await bot.add_roles(message.author, shit)
                await bot.send_message(message.channel, '**' + message.author.name + '** was shitposted pending manual approval.')
                msg = await bot.send_message(channel, message.author.mention + ', this role is commonly used by memers and raiders. Please contact admin/mod to regain access.')
                await asyncio.sleep(1)
                await bot.remove_roles(message.author, Snow1)
                await asyncio.sleep(1)
                await bot.remove_roles(message.author, Snow2)
                await asyncio.sleep(120)
                await bot.delete_message(msg)
                p = open(filePath + '.punish', 'w+')
                p.close()

############################
############################

    # If no on_message command invoked, check bot commands
    else:
        # https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
        await bot.process_commands(message)

############################
############################

@bot.event
async def on_member_join(member):

    sendWelcome = True

    # kicks new accounts to prevent raid
    if datetime.utcnow() - timedelta(hours=newAccount) < member.created_at:
        channel = discord.utils.get(member.server.channels, id = adminChan)
        await bot.send_message(member, 'Your account is too new to for "Coffee & Politics".  If you wish to join our discussions please wait a few days and try again.  :D')
        await bot.send_message(channel, '@here\nI kicked ' + member.mention + ' because account was made in the last ' + str(newAccount) + ' hours.')
        await bot.ban(member,0)
        sendWelcome = False

    # Checks for punishment evasion
    try:
        filePath = curDir + '/logs/db/' + str(member.id)

        # Looks for punish file
        t = open(filePath + '.punish')
        t.close()
        jail = discord.utils.get(member.server.roles, id = jailRole)
        Snow1 = discord.utils.get(member.server.roles, id = talkRole)
        Snow2 = discord.utils.get(member.server.roles, id = joinRole)
        embed=discord.Embed(title="User Jailed!", description="**{0}** was jailed for punishment evasion!".format(member), color=0xd30000)
        sendWelcome = False
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
    except:
        pass

    # Checks against ban list
    try:
        s = open(curDir + '/include/special')
        specialPeople = s.read().splitlines()
        s.close()
        sNum = len(specialPeople) - 1
        w = open(curDir + '/include/whitelist')
        whitelist = s.read().splitlines()
        w.close()

        if member.id in specialPeople and not member.id in whitelist:
            channel = discord.utils.get(member.server.channels, id = adminChan)
            await bot.send_message(channel, '@here\nI banned ' + member.mention + ' for stuff and things and reasons.')
            await bot.ban(member,0)
            sendWelcome = False
    except:
        pass

    # Looks for time file
    try:
        t = open(curDir + '/logs/db/' + mainServ + '.time')
        t.close()

        if sendWelcome:
            channel = discord.utils.get(member.server.channels, id = welcomeChan)
            await bot.send_message(channel, 'Hey ' + member.mention + ', welcome to **Coffee & Politics** \U0001F389\U0001F917 !')
            channel = discord.utils.get(member.server.channels, id = botChan)
            msg = await bot.send_message(channel, 'Welcome ' + member.mention + '! To access <#' + genChan + '> and other channels you need a role.\nIf you agree with <#' + ruleChan + '> give yourself an ideology role!\nExample:```.iam liberal\n.iamnot liberal```\nTo see available roles type `.LSAR`')
            await asyncio.sleep(600)
            await bot.delete_message(msg)
    except:
        if sendWelcome:
            channel = discord.utils.get(member.server.channels, id = adminChan)
            await bot.send_message(member, '**"Coffee & Politics"** is currently not accepting members at this time.  If you wish to join our discussions please wait a few days and try again.\nhttps://discord.gg/jpKHVyA')
            await bot.send_message(channel, '@here\n' + member.mention + ' tried to join but I kicked them because server is closed.  To open server, please `!disboard bump`.')
        await bot.kick(member)

@bot.event
async def on_member_remove(member):

    channel = discord.utils.get(member.server.channels, id = adminLogs)
    await bot.send_message(channel, 'Awww, ' + member.mention + ' just left the server \U0001F641')

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
