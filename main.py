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
import requests
import asyncio
import json
import sys
import os

timeout = 60*5  # 5 minutes
dateFormat = '%Y-%m-%d %H:%M:%S.%f'
newAccount = 72 # 48 hours

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, curDir + "/src/")

# Local modules
import zbdb

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
haRole = lines[32].rstrip()
logBackup = lines[33].rstrip()
afkChan = lines[34].rstrip()
repRole = lines[35].rstrip()
polChan = lines[36].rstrip()
voteChan = lines[37].rstrip()
ignoreServ = '533701082283638797'
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

#   Start of functions     #

############################
############################

def is_mod(m):
    with open(curDir + '/include/modRoles') as a:
        admin = [line.strip('\n').split(',') for line in a]
    for x in range(len(admin)):
        role = discord.utils.get(m.server.roles, id = admin[x-1][0])
        if role in m.author.roles:
            return True
    return False

def is_rep(m):
    rep = discord.utils.get(m.server.roles, id = repRole)
    if rep in m.author.roles:
        return True
    else:
        if is_mod(m):
            return True
    return False

def is_trusted(m):
    with open(curDir + '/include/trustedRoles') as t:
        trusted = [line.strip('\n').split(',') for line in t]
    for x in range(len(trusted)):
        role = discord.utils.get(m.server.roles, id = trusted[x-1][0])
        if role in m.author.roles:
            return True
    return False

def is_political(m):
    with open(curDir + '/include/polRoles') as p:
        political = [line.strip('\n').split(',') for line in p]
    for x in range(len(political)):
        role = discord.utils.get(m.server.roles, id = political[x-1][0])
        if role in m.author.roles:
            return True
    return False

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

def is_serious(m):
    serious = discord.utils.get(m.author.server.roles, id = seriousRole)
    if serious in m.author.roles:
        return True
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

def is_polchan(m):
    if m.channel.id == polChan:
        return True
    return False

def is_polenabled(m):
    if m.channel.id == shetChan:
        return True
    if m.channel.id == adminChan:
        return True
    if m.channel.id == voteChan:
        return True
    return False

def is_invite(m):
    if '://discord.gg' in m.content.lower():
        return True
    if 'disboard.org/server/' in m.content.lower():
        return True
    if '://discord.me/' in m.content.lower():
        return True
    if '://discordapp.com/invite/' in m.content.lower():
        return True
    return False

def is_caps(m): # 70%+ caps
    stripped = m.content.replace(' ','')
    allLetters = len(stripped)
    if allLetters < 10:
        return False
    capLetters = sum(1 for c in m.content if c.isupper())
    percentage = capLetters / allLetters
    if percentage >= 0.70:
        return True
    return False

def is_aids(m): # too many spoilers
    message = m.content
    if sum(x is "|" for x in message) > 10:
        return True
    return False

def is_in_trouble(m):
    try:
        filePath = curDir + '/logs/db/' + str(m.id)

        # Looks for punish file
        t = open(filePath + '.punish')
        t.close()
        return True
    except:
        return False

def is_kicked(m):
    filePath = curDir + '/logs/db/' + str(m.id)
    try:
        # Looks for punish file
        t = open(filePath + '.kicked')
        t.close()

        p = open(filePath + '.punish', 'w+')
        p.close()
        return True
    except:
        t = open(filePath + '.kicked', 'w+')
        t.close()
        return False


# Message ignore check
def is_ignore(m):
    if '.iamz' in m.content.lower():
        return True
    return False

# member or author object
def get_avatar(m):
    if m.avatar_url is '':
        pfp = m.default_avatar_url
    else:
        pfp = m.avatar_url
    return pfp

def num_roles(m):
    x = len(list(m.author.roles))
    return x

async def remove_roles(m, out):
    # Roles to Remove
    filePath = curDir + '/logs/db/' + m.id
    Snow1 = discord.utils.get(m.server.roles, id = talkRole)
    Snow2 = discord.utils.get(m.server.roles, id = joinRole)
    shit = discord.utils.get(m.server.roles, id = shetRole)
    jail = discord.utils.get(m.server.roles, id = jailRole)
    mute = discord.utils.get(m.server.roles, id = muteRole)
    old = discord.utils.get(m.server.roles, id = oldRole)
    serious = discord.utils.get(m.server.roles, id = seriousRole)

    # Look for working file, if not found make one
    try:
        w = open(filePath + '.working')
        w.close()

        w = open(filePath + '.working', 'w+')
        w.write(out)
        w.close
        return
    except:
        w = open(filePath + '.working', 'w+')
        w.write(out)
        w.close

    # Remove all roles
    await bot.remove_roles(m, Snow1)
    await asyncio.sleep(1)
    await bot.remove_roles(m, Snow2)
    await asyncio.sleep(1)
    await bot.remove_roles(m, shit)
    await asyncio.sleep(1)
    await bot.remove_roles(m, jail)
    await asyncio.sleep(1)
    await bot.remove_roles(m, mute)
    await asyncio.sleep(1)
    await bot.remove_roles(m, old)
    await asyncio.sleep(1)
    await bot.remove_roles(m, serious)
    await asyncio.sleep(1)

    # Try to open new updated working file
    try:
        f = open(filePath + '.working')
        info = f.readlines()
        out = info[0].rstrip()
        f.close()
    except:
        pass

    # add last chosen role
    if out == 'mute':
        await bot.add_roles(m, mute)
    elif out == 'jail':
        await bot.add_roles(m, jail)
    elif out == 'shitpost':
        await bot.add_roles(m, shit)
    else:
        await bot.add_roles(m, Snow1)

    # Remove working files
    os.remove(filePath + '.working')
    return

async def punish_shitpost(m):
    if m.server.id == mainServ and not is_rep(m):
        filePath = curDir + '/logs/db/' + m.author.id
        shit = discord.utils.get(m.author.server.roles, id = shetRole)
        Snow1 = discord.utils.get(m.author.server.roles, id = talkRole)
        Snow2 = discord.utils.get(m.author.server.roles, id = joinRole)
        old = discord.utils.get(m.author.server.roles, id = oldRole)
        serious = discord.utils.get(m.author.server.roles, id = seriousRole)
        embed=discord.Embed(title="Shitposter!", description="**{0}** was given Shitposter by **ZigBot#1002**!".format(m.author), color=0xd30000)
        channel = discord.Object(id=shetChan)
        msg = '<@' + m.author.id + '>'
        await bot.send_message(channel, 'Looks like you pushed it too far ' + msg + '. You live here now. Enjoy!!')
        # await bot.say(embed=embed)
        await bot.send_message(discord.Object(id=logAct),embed=embed)
        await bot.add_roles(m.author, shit)
        await asyncio.sleep(1)
        await bot.remove_roles(m.author, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(m.author, Snow2)
        await asyncio.sleep(1)
        await bot.remove_roles(m.author, old)
        await asyncio.sleep(1)
        await bot.remove_roles(m.author, serious)

        # punishment evasion
        p = open(filePath + '.punish', 'w+')
        p.close()

        # Kick from voice channel
        kick_channel = discord.Object(id=afkChan)
        await bot.move_member(m.author, kick_channel)
    return

async def log_backup_embed(e):
    if logBackup is not '':
        channel = discord.Object(id=logBackup)
        await bot.send_message(channel, embed=e)

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

############################
############################
############################
############################
############################
############################

@bot.event
async def on_message(message):
    # Stops bot from replying to self
    if message.author == bot.user or message.author.bot:
        return

#    with open(curDir + '/include/special') as a:
#        special = [line.strip('\n').split(',') for line in a]
#    #TODO: [var] is not good solution
#    if [str(message.author.id)] in special:
#        print('found ' + str(message.name))

    no = discord.Object(id=ignoreServ)
    if message.server is no:
        return

############################
############################

    if is_legacy(message) and not is_in_trouble(message):
        serious = discord.utils.get(message.author.server.roles, id = seriousRole)
        await bot.add_roles(message.author, serious)

#++++++++++++++++++++++++++#
#++++++++++++++++++++++++++#

    if is_mod(message):
        pass
    elif is_trusted(message):
        pass
    else:
        if is_invite(message) and message.server.id == mainServ:
            embed=discord.Embed(title="Banned!", description="**{0}** was given Banned by **ZigBot#1002** for violation of rule 8!".format(message.author), color=0xd30000)
            await bot.send_message(discord.Object(id=logAct),embed=embed)
            await bot.send_message(message.author, 'It\'s in the rules, no sharing discord links.\n Bye bye!')
            await bot.ban(message.author)
            # await bot.kick(message.author)
            await bot.delete_message(message)
            return
        if is_aids(message) and int(message.channel.id) != int(shetChan):
            msg = await bot.send_message(message.channel, 'Alright, ' + message.author.mention + ' stop abusing the new toy.')
            await bot.delete_message(message)
            await asyncio.sleep(10)
            await bot.delete_message(msg)
        if is_caps(message) and int(message.channel.id) != int(shetChan):
            await bot.send_message(message.channel, 'Alright, ' + message.author.mention + ' has been warned for \'**Capital letters**\'.')
        if len(message.mentions) >= 5:
            await bot.send_message(message.channel, 'Alright, ' + message.author.mention + ' has been shitposted for \'**Mass mentions**\'.')
            await punish_shitpost(message)

#++++++++++++++++++++++++++#
#++++++++++++++++++++++++++#

    # if is_caps(message):
    #     lowered = message.content.lower()
    #     msg = await bot.send_message(message.channel, "||*turns caps off*|| " + str(message.author) + " ***Said:*** - " + lowered)
    #     await bot.delete_message(message)
    #     if not is_mod:
    #         await asyncio.sleep(60)
    #         await bot.delete_message(msg)

    # if message.content.lower().startswith('!refuel'):
    #     msg = await bot.send_message(message.channel,'Helicopter is refueled and ready to... physically remove... so to speak...\nhttps://cdn.discordapp.com/attachments/509245339664908299/522448178138578964/1512796577930.gif')
    #     await bot.delete_message(message)
    #     await asyncio.sleep(timeout)
    #     await bot.delete_message(msg)

    if is_polchan(message):
        if message.content.lower().startswith('poll:'):
            await bot.add_reaction(message, '\U0001F44D')
            await bot.add_reaction(message, '\U0001F44E')
            await bot.add_reaction(message, '\U0001F937')
        else:
            msg = await bot.send_message(message.channel, '**Your message will be removed. __Copy it now!__**\nYou can read this message after you copy yours.\n\nThis is not in a valid poll format "Poll: ".\nIf this was  poll, please type "Poll: " first, then paste in your message.\nIf this is not a poll, continue the discussion in <#549269596926902282>.\nThank you.')
            await asyncio.sleep(30)
            await bot.delete_message(message)
            await asyncio.sleep(60)
            await bot.delete_message(msg)

    if is_polenabled(message):
        if message.content.lower().startswith('poll:'):
            await bot.add_reaction(message, '\U0001F44D')
            await bot.add_reaction(message, '\U0001F44E')
            await bot.add_reaction(message, '\U0001F937')

    if ' iq' in message.content.lower() or 'iq ' in message.content.lower():
        msg = await bot.send_message(message.channel, message.author.mention + ', there are better arguments than IQ to make your case.\nhttps://www.independent.co.uk/news/science/iq-tests-are-fundamentally-flawed-and-using-them-alone-to-measure-intelligence-is-a-fallacy-study-8425911.html\nhttps://www.cell.com/neuron/fulltext/S0896-6273(12)00584-3')
        await asyncio.sleep(timeout)
        await bot.delete_message(msg)

    # if 'smart' in message.content.lower():
    #     x = randint(0,5)
    #     brainletURL = brainlet[x].rstrip()
    #     msg = await bot.send_message(message.channel, 'I is r b smartr den u.\n' + brainletURL)
    #     await asyncio.sleep(5)
    #     await bot.delete_message(msg)

    # if message.content.startswith('!disboard bump'):
    #     # Needed vars
    #     bumServ = message.server.id
    #     bumChan = message.channel.id
    #     bumMemb = message.author.id
    #     channel = discord.Object(id=bumChan)
    #     curTime = datetime.now()
    #     newTime = datetime.now() + timedelta(hours=2)
    #     filePath = curDir + '/logs/db/' + bumServ

    #     # Replaces member and channel
    #     # Old info not needed only updated
    #     oldMemb = open(filePath + '.member', 'w+')
    #     oldMemb.write("%s\r\n" % (bumMemb))
    #     oldMemb.close()
    #     oldChan = open(filePath + '.channel', 'w+')
    #     oldChan.write("%s\r\n" % (bumChan))
    #     oldChan.close()

    #     # Loads existing needed time data
    #     # If not found, creates data
    #     try:
    #         t = open(filePath + '.time')
    #         tStrip = t.readlines()
    #         oldTime = tStrip[0].rstrip()
    #     except:
    #         t = open(filePath + '.time', 'w+')
    #         t.write("%s\r\n" % (str(newTime)))
    #         oldTime = str(newTime)
    #     t.close()

    #     lastBump = datetime.strptime(oldTime, dateFormat)

    #     # Tests if 2 hours has passed
    #     # If not, it lets you know it'll remind you later
    #     # It always updates member and channel
    #     if curTime < lastBump:
    #         diff = int(int((lastBump - curTime).seconds)/60) + 1
    #         await bot.send_message(channel, 'I\'ll remind you to bump here in ' + str(diff) + ' minutes.')
    #     else:
    #         await bot.send_message(channel, 'I\'ll remind you in 120 mins to bump disboard again.')
    #         t = open(filePath + '.time', 'w+')
    #         t.write("%s\r\n" % (str(newTime)))
    #         t.close()

    # # allow disboard bump stop
    # if message.content.startswith('!disboard stop') and message.author.server_permissions.administrator:
    #     disboard = discord.utils.get(message.server.members, name='DISBOARD')
    #     bumServ = message.server.id
    #     bumChan = message.channel.id
    #     filePath = curDir + '/logs/db/' + bumServ
    #     channel = discord.Object(id=bumChan)
    #     msg = await bot.wait_for_message(timeout=3, author=disboard)
    #     try:
    #         os.remove(filePath + '.time')
    #         await bot.delete_message(msg)
    #         await bot.send_message(channel, 'I\'ll stop reminding you for now. `!disboard bump` to start again.')
    #     except:
    #         await bot.send_message(channel, 'I\'m already set to not remind you. Please `!disboard bump` to start again.')

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
                await asyncio.sleep(2e-2)
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
            await asyncio.sleep(2e-2)
        rmRole = discord.utils.get(message.server.roles, id = busyRole)
        await bot.remove_roles(message.author, rmRole)

        try:
            os.remove(filePath + '.busy')
        except:
            pass
        await bot.delete_message(message)
        return

    if message.content.lower().startswith('owo') and str(message.author.id) == '164869272697438209':
        print('It\'s working')

    if message.content.lower().startswith('.iam'):
        if message.content.lower().startswith('.iamz') and is_zig(message):
            zigBot = discord.utils.get(message.server.roles, id = botRole)
            if not zigBot in message.author.roles:
                await bot.add_roles(message.author, zigBot)
                await bot.delete_message(message)
            else:
                await bot.remove_roles(message.author, zigBot)
                await bot.delete_message(message)
            return
        elif message.content.lower().startswith('.iamz'):
            await bot.send_message(message.channel, message.author.mention + ' You\'re not Zig.')
            return
        if message.content.lower().startswith('.iam epic') and is_cheeti(message):
            zigBot = discord.utils.get(message.server.roles, id = botRole)
            if not zigBot in message.author.roles:
                msg = await bot.send_message(message.channel,'You\'re epic!')
                await asyncio.sleep(timeout)
                await bot.delete_message(msg)
                await bot.delete_message(message)
            else:
                msg = await bot.send_message(message.channel,'You\'re epic!')
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
            if not is_political(message):
                # User removed role, revert
                msg = await bot.send_message(message.channel, 'You aren\'t allowed to chat without an ideology.  Please choose a role from #roles or `.lsar`')
                await bot.add_roles(message.author, Snow2)
                await asyncio.sleep(1)
                await bot.remove_roles(message.author, Snow1)
                await asyncio.sleep(7)
                await bot.delete_message(msg)
                await bot.delete_message(message)

        # Checks for initial role to remove undecided
        elif discord.utils.get(message.author.roles, id = talkRole) is None and discord.utils.get(message.author.roles, id = joinRole) is not None and is_political(message):
            await bot.add_roles(message.author, Snow1)
            await asyncio.sleep(1)
            await bot.remove_roles(message.author, Snow2)

        # If role doesn't exist
        elif not is_political(message):
            if discord.utils.get(message.author.roles, id = busyRole) is None:
                msg = await bot.send_message(message.channel, 'Please choose a political role from #roles or `.lsar`')
            else:
                msg = await bot.send_message(message.channel, 'Your status is still set to busy.\n Please `.iamn busy` to get your roles back.')
            await asyncio.sleep(7)
            await bot.delete_message(msg)
            await bot.delete_message(message)

        # Checks for meme roles to shitpost
        message.content = message.content.lower()
        for x in range(len(memeRoles)):
            if message.content.startswith(memeRoles[x-1]) and not is_serious(message):
                filePath = curDir + '/logs/db/' + message.author.id
                shit = discord.utils.get(message.server.roles, id = shetRole)
                Snow1 = discord.utils.get(message.server.roles, id = talkRole)
                Snow2 = discord.utils.get(message.server.roles, id = joinRole)
                channel = discord.Object(id=shetChan)
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
    no = discord.Object(id=ignoreServ)
    if member.server is no:
        return

    sendWelcome = True
    Snow2 = discord.utils.get(member.server.roles, id = joinRole)

    # Member join log
    # embed=discord.Embed(description=member.mention + " " + member.name, color=0x23d160)
    # embed.add_field(name="Account Creation Date", value=member.created_at, inline=False)
    # pfp = get_avatar(member)
    # embed.set_thumbnail(url=pfp)
    # embed.set_author(name="Member Joined", icon_url=pfp)
    # embed.set_footer(text="ID: " + member.id + " • Today at " + f"{datetime.now():%I:%M %p}")
    # await bot.send_message(discord.Object(id=adminLogs),embed=embed)
    # await log_backup_embed(embed)

    # kicks new accounts to prevent raid
    if datetime.utcnow() - timedelta(hours=newAccount) < member.created_at:
    #     channel = discord.utils.get(member.server.channels, id = adminChan)
    #     await bot.send_message(member, 'Your account is too new to for "Coffee & Politics".  If you wish to join our discussions please wait a few days and try again.  :D')
    #     await bot.send_message(channel, '@here\nI kicked ' + member.mention + ' because account was made in the last ' + str(newAccount) + ' hours.')
    #     await bot.ban(member,0)
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
        try:
            k = open(filePath + '.kicked')
            k.close()
            sendWelcome = True
        except:
            embed=discord.Embed(title="User Jailed!", description="**{0}** was jailed for punishment evasion!".format(member), color=0xd30000)
            await bot.send_message(discord.Object(id=logAct),embed=embed)
            sendWelcome = False
        # await bot.say(embed=embed)
        await bot.add_roles(member, jail)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow1)
        await asyncio.sleep(1)
        await bot.remove_roles(member, Snow2)
    except:
        pass

    with open(curDir + '/include/special') as txt:
        specialPeople  = [line.strip('\n').split(',') for line in txt]
    with open(curDir + '/include/whitelist') as txt:
        whitelist = [line.strip('\n').split(',') for line in txt]

    if [str(member.id)] in specialPeople and not [str(member.id)] in whitelist:
    #     channel = discord.utils.get(member.server.channels, id = adminChan)
    #     await bot.send_message(channel, '@here\nI banned ' + member.mention + ' for stuff and things and reasons.')
    #     await bot.ban(member,0)
        sendWelcome = False

    # Looks for time file
    try:
        t = open(curDir + '/logs/db/' + mainServ + '.time')
        t.close()

        if sendWelcome:
            # await bot.add_roles(member, Snow2)
            # channel = discord.utils.get(member.server.channels, id = welcomeChan)
            # await bot.send_message(channel, 'Hey ' + member.mention + ', welcome to **Coffee & Politics** \U0001F389\U0001F917 !')
            channel = discord.utils.get(member.server.channels, id = botChan)
            msg = await bot.send_message(channel, 'Welcome ' + member.mention + '! To access <#' + genChan + '> and other channels you need a political role.\n(If you are learning select the learning role)\nIf you agree with <#' + ruleChan + '> give yourself an ideology role!\nExample:```.iam conservative\n.iamnot conservative```\nTo see available roles type `.LSAR`\n\nWe understand these may be painful instructions for a few people to follow.\nThose people include but not limited to:\nTrolls\nChildren\nPeople who can\'t read\nPeople who want to learn but can\'t read\n\nNot every community is for you.')
            await asyncio.sleep(600)
            await bot.delete_message(msg)
    except:
        # if sendWelcome:
        #     channel = discord.utils.get(member.server.channels, id = adminChan)
        #     if is_in_trouble(member):
        #         await bot.send_message(member, '**"Coffee & Politics"** has banned you for being unable to read. Sorry, go play roblox elsewhere.')
        #         await bot.send_message(channel, '@here\n' + member.mention + ' can\'t read so I banned them.')
        #         await bot.ban(member)
        #     elif is_kicked(member):
        #         await bot.send_message(member, '**"Coffee & Politics"** is currently not accepting members at this time.  If you wish to join our discussions please wait a few days and try again.\nhttps://discord.gg/xVtZbn8')
        #         await bot.send_message(channel, '@here\n' + member.mention + ' tried to join but I kicked them because server is closed.  To open server, please `!disboard bump`.')
        #     else:
        #         await bot.send_message(member, '**"Coffee & Politics"** is currently not accepting members at this time.  If you wish to join our discussions please wait a few days and try again.\nhttps://discord.gg/xVtZbn8')
        #         await bot.send_message(channel, '@here\n' + member.mention + ' tried to join but I kicked them because server is closed.  To open server, please `!disboard bump`.')
        pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    servers = list(bot.servers)
    for x in range(len(servers)):
        print("    " + servers[x-1].id + " - " + servers[x-1].name + " (Members: " + str(len(servers[x-1].members)) + ")")

bot.run(TOKEN)
