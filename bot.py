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
import sqlite3
import datetime

# connecting to Twitch IRC 
HOST = "irc.twitch.tv"  
NICK = "ardahbot" 
CHAN = 'jereck00'  # channel name 
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
s.connect((HOST, PORT))
s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("JOIN #%s\r\n" % CHAN, "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))

def socketconnection(): 
    s.connect((HOST, PORT))
    s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAN, "UTF-8"))
    s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
    s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
    s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))

if os.path.exists("{}DB.db".format(CHAN)):
    dbcon = sqlite3.connect("{}DB.db".format(CHAN))
    cursor = dbcon.cursor()
else:
    dbcon = sqlite3.connect("{}DB.db".format(CHAN))
    cursor = dbcon.cursor()
    cursor.execute('CREATE TABLE channelPoints(username text PRIMARY KEY,points INT DEFAULT 0)')
    dbcon.commit()

#globals
duel_list = {}
memeteam = ["jereck00", "shin0l", "leo_n_milk"]

def tablereport():
    global dbcon
    global cursor

    for x in cursor.execute('SELECT * from channelPoints ORDER BY points'):
        sendmessage(x)

def requestpoints(message):
    global dbcon
    global cursor
    
    messagelist = message.split()
    index = messagelist.index('!points')
    if len(messagelist) == 1:
        u = username
    elif len(messagelist) == 2:
        u = messagelist[index+1]
    cursor.execute('SELECT points FROM channelPoints WHERE username=?',((u,)))
    sendmessage(cursor.fetchone())


def givepoints(message):
    global dbcon
    global cursor

    messagelist = message.split()
    index = messagelist.index('!givepoints')
    u = str(messagelist[index+1])
    p = messagelist[index+2]

    cursor.execute('UPDATE channelPoints SET points=points+? WHERE username=?',(p, u))
    dbcon.commit()
    sendmessage("{} has been given {} points".format(u, p))


def sendmessage(text):
    # Method for sending a message
    s.send(bytes("PRIVMSG #" + CHAN + " :" + str(text) + "\r\n", "UTF-8"))


def timeout(user, secs):
    timeout_message = "PRIVMSG #" + CHAN + ": /timeout %s %s\r\n" % (user, secs)
    s.send(bytes(timeout_message), "UTF-8")


def puppet():
    while True:
        message = input(' assuming direct control: ') 
        sendmessage(message)
        commands(message, 'ardahBot')
        
    
    
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

def duel(challenger, target):
    global duel_list
    duel_list[target] = challenger
    duelMessage = '/me {} has challenged {} to a duel PogChamp type !accept to confirm duel'.format(challenger, target)
    sendmessage(duelMessage)


def cointoss(username):
    global duel_list
    coin = random.randint(0, 1)
    if coin == 0:
        victory_message = '/me {} has won the duel against {}! PogChamp'.format(username, duel_list[username])
        sendmessage(victory_message)
    if coin == 1:
        defeat_message = '/me {} has defeated {} in a duel! PogChamp'.format(duel_list[username], username)
        sendmessage(defeat_message)
        sendmessage('Never lucky BabyRage')
    del duel_list[username] 


def commands(message, username):
    global duel_list
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

    if '!duel' in message:
        messageList = message.split()
        messageList = [e.lower() for e in messageList]
        index = messageList.index('!duel')

        if messageList[index+1] not in duel_list:
            duel(username, messageList[index+1])
        else:
            del duel_list[messageList[index+1]]
            duel(username, messageList[index+1]) 

        if messageList[index+1] == 'ardahBot'.lower():
            time.sleep((random.randint(1, 3)))
            sendmessage('!accept')
            cointoss('ardahbot')

    if message == '!accept' and username in duel_list:
        time.sleep((random.randint(0,1)))
        cointoss(username) 

    if message == '!decline' and username in duel_list:
        decline_message = '{} has declined the duel with {}'.format(username, duel_list[username])
        sendmessage(decline_message)
        del duel_list[username]
        
    if message == '!clearduels' and username == 'jereck00':
        duel_list = {} 
        sendmessage('clearing duel list')

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

    if message == '!github':
        sendmessage('https://github.com/deandrehall/ardahBot')
        
    if '!lookup' in message:
        region = 'NA'
        messageList = message.split()
        index = messageList.index('!lookup')
        messageList.remove(index)
        summonerName = ' '.join(messageList)
        responseJSON  = requestSummonerData(region, summonerName, APIKey)
        ID = responseJSON[summonerName]['id']
        ID = str(ID)
        responseJSON2 = requestRankedData(region, ID, APIKey)
        rank = responseJSON2[ID][0]['tier']
        rank += " %s" % responseJSON2[ID][0]['entries'][0]['division']
#sendmessage(rank)
        sendmessage("{} {} LP".format(rank, responseJSON2[ID][0]['entries'][0]['leaguePoints']))

    if '!test' in message and username == 'jereck00':
        tablereport() 

    if '!points' in message:
        requestpoints(message)

    if '!givepoints' in message and username == 'jereck00':
        givepoints(message)

    if message == '!reconnect' and username == 'jereck00':
        socketconnection()

print('it that bot MrDestructoid')
t = threading.Thread(target=puppet).start()

while True: 
    try:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
        temp = str.split(readbuffer, "\n")
        readbuffer = temp.pop() 

        for line in temp:
            # Checks whether the message is PING because its a method of Twitch to check if you're afk
            if(line[0] == "PING"):
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
            else:
                # Splits the given string so we can work with it better
                parts = str.split(line, ":")

                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = str.split(parts[1], "!")
                username = usernamesplit[0]
                
                cursor.execute('INSERT OR IGNORE INTO channelPoints (username, points) VALUES (?,?)',(username,'0'))
                dbcon.commit()

                print(username + ": " + message)
                commands(message, username.lower())

    except KeyboardInterrupt:
        raise
    except:
        print(traceback.format_exc())
                    
               
