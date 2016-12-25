import socket
import string
import random
import time
import json
import threading
import os
import traceback
import re
import requests
import sys
from collections import deque

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"  # irc.twitch.tv
NICK = "ardahbot"
CHAN = 'jereck00'  # Name of your channel
PORT = 6667
PASS = "oauth:3hfhwlewgv2ydwkhohs6udttriheuo"
readbuffer = ""
MODT = False


CHANNEL_NAME = CHAN
CHANNEL_NAME = CHANNEL_NAME.lower()
SLEEP_TIME = 120
IRC_CHANNEL = "#" + CHANNEL_NAME

APIKey = "RGAPI-c2b5b567-5229-46e9-b7b8-7eb218c1ea8f"

HOST2 = "199.9.253.119"

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
#s2 = socket.socket()
s.connect((HOST, PORT))
#s2.connect((HOST2, PORT))
s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("JOIN #%s\r\n" % CHAN, "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
# connecting to the bot's chat group so that whispers work
"""
s2.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
s2.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s2.send(bytes("JOIN #_ardahbot_1454310601454\r\n", "UTF-8"))
s2.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s2.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
s2.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
"""

# garbage vars bc im garbage at python
duel_list = deque([])
defender = ''
duel_check = False
followsDict = {}
modsDict = {}
points = {}
memeteam = ["jereck00", "shin0l", "leo_n_milk"]

def sendmessage(text):
    # Method for sending a message
    s.send(bytes("PRIVMSG #" + CHAN + " :" + str(text) + "\r\n", "UTF-8"))


def sendSecret(username):
    s2.send(bytes("PRIVMSG #ardahBot :.w " + username + " nice\r\n", "UTF-8"))


def timeout(user, secs):
    timeout_message = "PRIVMSG #" + CHAN + ": /timeout %s %s\r\n" % (user, secs)
    s.send(bytes(timeout_message), "UTF-8")
    
    
def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()


def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()


def generatememe():
    fill = "XX"
    empty = "__"
    height = 8
    width = 8
    fillpercent = 0.4
    halfwidth = int(width / 2)
    painted = 0
    maxPainted = height * halfwidth * fillpercent
    adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]
    meme = [[empty for w in range(halfwidth)] for h in range(height)]
    y, x = random.randint(0, height - 1), random.randint(0, halfwidth - 1)
    lst = [(y, x)]
    while len(lst) != 0:
        y, x = lst.pop()
        if painted <= maxPainted:
            meme[y][x] = fill
            painted += 1
            random.shuffle(adjacent)
            for posy, posx in adjacent:
                tmpy, tmpx = y + posy, x + posx
                if tmpx >= 0 and tmpx < halfwidth:
                    if tmpy >= 0 and tmpy < height:
                        if meme[tmpy][tmpx] is not fill:
                            lst.append((tmpy, tmpx))
    for h in range(height):
        half = ""
        for w in range(halfwidth):
            half += meme[h][w]
        identicon = (half + half[::-1])
        sendmessage(identicon)


def follows(username):
    followsList = []

    if username in followsDict:
        return followsDict[username]

    else:
        URL = "https://api.twitch.tv/kraken/channels/" + CHAN + "/follows"
        followJson = requests.get(URL).json()

        for counter in range(0, len(followJson["follows"])):
            item = str(followJson["follows"][counter]["user"]["name"])
            followsList.append(item)

            if item in followsList:
                followsDict[item] = True
            else:
                followsDict[item] = False

        if username in followsList:
            return followsDict[username]
        else:
            return False


def numChatters():
    r = urllib2.urlopen("http://tmi.twitch.tv/group/user/" + CHAN + "/chatters")
    viewingJson = json.loads(r.read())
    return viewingJson["chatter_count"]


def chatting(username):
    viewerList = []

    r = urllib2.urlopen("http://tmi.twitch.tv/group/user/" + CHAN + "/chatters")
    viewingJson = json.loads(r.read())

    for item in viewingJson["chatters"]["moderators"]:
        viewerList.append(str(item))

    for item in viewingJson["chatters"]["staff"]:
        viewerList.append(str(item))

    for item in viewingJson["chatters"]["admins"]:
        viewerList.append(str(item))

    for item in viewingJson["chatters"]["global_mods"]:
        viewerList.append(str(item))

    for item in viewingJson["chatters"]["viewers"]:
        viewerList.append(str(item))

    if username in viewerList:
        return True
    else:
        return False


def anotherdog():
    time.sleep(0.4)
    hotdogyes = random.randint(1, 4)
    if hotdogyes == 1:
        sendmessage('no more dogs')
    else:
        sendmessage('=(~~~)=')
        anotherdog()


def anotherdoodle():
    time.sleep(0.4)
    doodleyes = random.randint(1, 4)
    if doodleyes == 1:
        sendmessage('no more doodle for n8 lmao')
    else:
        sendmessage('8=D')
        anotherdoodle()


def commands(message, username):
    if message == "!secret":
        sendSecret(username)

    if message == "!meme":
        sendmessage("EleGiggle")

    if message == "!sliced":
        sendmessage("**unsheathes katana**")

    if message == "!whoami":
        sendmessage(username)

    if message == "!corn":
        sendmessage(
            "https://33.media.tumblr.com/b07644c8da2e4b15c6119d37078d2e16/tumblr_n6kja1gWkE1qln00mo2_400.gif")

    if message == "!hotdog":
        sendmessage("Kreygasm")

    if message == "!sudoku":
        print('kicking %s from chat') % username
        sendmessage("He will be missed...")
        timeout_message = "PRIVMSG #" + CHAN + " :/timeout %s %s\r\n" % (username, 30)
        s.send(timeout_message)
        s2.send("PRIVMSG #ardahBot :.w " + username + " rip 2 u\r\n")

    if message == "!uptime":
        sendmessage('dre hasn\'t figured out how to implement this command yet lmao')
        time.sleep(.5)
        sendmessage('If you have the BetterTwitchTV extension you can type /uptime')

    if '!duel' in message and len(duel_list) == 0:
        duel_list.append(username)
        duel_list.append(message[6:])
        duel_message = '/me %s has challenged %s to a duel PogChamp type !accept to confirm duel' % (
            duel_list[0], duel_list[1])
        sendmessage(duel_message)

    if len(duel_list) == 2 and username == duel_list[1] and message == '!accept':
        coin = random.randint(0, 1)
        if coin == 0:
            victory_message = '/me %s has won the duel against %s! PogChamp' % (
                duel_list[0], duel_list[1])
            sendmessage(victory_message)
        if coin == 1:
            defeat_message = '/me %s has defeated %s in a duel! PogChamp' % (duel_list[1], duel_list[0])
            sendmessage(defeat_message)
            sendmessage('Never lucky BabyRage')
            duel_list.popleft()
            duel_list.popleft()

    if message == '!cancelduel' and username == duel_list[0] and len(duel_list) == 2:
        cancel_duel_message = '%s has canceled the duel' % (duel_list[0])
        sendmessage(cancel_duel_message)
        duel_list.popleft()
        duel_list.popleft()

    if '!duel' in message and username not in duel_list:
        if message[6:] == duel_list[0]:
            duel_in_progress = '%s currently has a duel pending' % (duel_list[0])
            suggest_cancel = '%s can cancel the pending duel by typing !cancelduel' % (duel_list[0])
            sendmessage(duel_in_progress)
            sendmessage(suggest_cancel)
        if message[6:] == duel_list[1]:
            duel_in_progress = '%s currently has a duel pending' % (duel_list[1])
            suggest_cancel = '%s can cancel the pending duel by typing !cancelduel' % (duel_list[1])
            sendmessage(duel_in_progress)
            sendmessage(suggest_cancel)

    if message == '!decline' and len(duel_list) == 2 and username == duel_list[1]:
        decline_message = '%s has declined the duel with %s' % (duel_list[1], duel_list[0])
        sendmessage(decline_message)
        duel_list.popleft()
        duel_list.popleft()

    if '!duel' in message and len(duel_list) == 2 and username not in duel_list:
        sendmessage('The duel list is currently full. Please wait until the pending duel has completed')

    if '!duel' in message and message[6:] == 'ardahbot':
        time.sleep((random.randint(1, 3)))
        sendmessage('!accept')
        coin = random.randint(0, 1)
        if coin == 0:
            victory_message = '/me %s has won the duel against %s! PogChamp' % (
                duel_list[0], duel_list[1])
            sendmessage(victory_message)
        if coin == 1:
            defeat_message = '/me %s has defeated %s in a duel! PogChamp' % (duel_list[1], duel_list[0])
            sendmessage(defeat_message)
            sendmessage('Never lucky BabyRage')
        duel_list.popleft()
        duel_list.popleft()

    if message == '!clearduels' and username == 'jereck00':
        duel_list[:] = []
        sendmessage('clearing duel queue')

    if message == '!n8iscool':
        sendmessage('http://i.imgur.com/fcWhKyU.jpg')

    if message == '!nice' and username in memeteam:
        sendmessage(
            'https://38.media.tumblr.com/1f1ea822c3b32719c382d775c629713a/tumblr_mwzoseIvD01sedjuto1_500.gif')

    if message == '!hotdogs' and username == 'n8many':
        sendmessage('looks like n8 wants some hotdogs...')
        sendmessage('8=D')
        anotherdoodle()

    if message == '!hotdogs' and username != 'n8many':
        sendmessage('looks like %s is playing the hotdog game, how many dogs will they get?' % username)
        sendmessage('=(~~~)=')
        anotherdog()

    if message == '!draw':
        generatememe()

    if '!following' in message:
        name = message[11:]
        if follows(name.lower()):
            sendmessage("%s is following the channel!" % name)
        else:
            sendmessage("%s is not following the channel DansGame" % name)

    if '!chatting' in message:
        name = message[10:]
        if chatting(name):
            sendmessage("%s is with us" % name)
        else:
            sendmessage("%s is not with us" % name)

    if message == '!github':
        sendmessage('https://github.com/deandrehall/ardahBot')

    if message == '!countviewers':
        numCurrentChatters = str(numChatters())
        sendmessage("There are currently %s registered users in the chat" % numCurrentChatters)
        
    if '!lookup' in message:
        region = 'NA'
        summonerName = message[8:]
        responseJSON  = requestSummonerData(region, summonerName, APIKey)
        ID = responseJSON[summonerName]['id']
        ID = str(ID)
        responseJSON2 = requestRankedData(region, ID, APIKey)
        rank = responseJSON2[ID][0]['tier']
        rank += " %s" % responseJSON2[ID][0]['entries'][0]['division']
#sendmessage(rank)
        sendmessage("{} {} LP".format(rank, responseJSON2[ID][0]['entries'][0]['leaguePoints']))

    if '!test' in message:
        messageList = message.split()
        index = messageList.index('!test')
        sendmessage("command = {} arg1 = {} arg2 = {}".format(messageList[index], messageList[index+1],messageList[index+2]))
 
		
sendmessage('it that bot')

def getUser(line):
    username = ""
    usernamesplit = str.split(parts[1], "!")
    username = usernamesplit[0]
    return username

def getMessage(line):
    try:
        message = parts[2][:len(parts[2]) - 1]
    except:
        message = ""
    return message


def parseMessage(parts):
    try:
        username = getUser(parts)
        message = getMessage(parts)
    
        if MODT:
            print(username + ": " + message)
            commands(message, username) 

    except:
        print(traceback.format_exc())

while True:
    try:
        readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:

            if (line[0] == "PING"):
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8")) 
            else:
                parts = str.split(line, ":")

                parseMessage(parts)

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
            
    except:
        print(traceback.format_exc())
