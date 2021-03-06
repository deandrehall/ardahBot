#!/usr/bin/python3

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

#pulls channel name from the commandline. if there is no arg, channel name defaults to jereck00
try:
    CHAN = sys.argv[1]
except:
    CHAN = 'jerecktone'

# connecting to Twitch IRC 
HOST = "irc.twitch.tv"  
NICK = "ardahbot"  
PORT = 6667
PASS = sys.argv[2]
readbuffer = ""
MODT = False

CHANNEL_NAME = CHAN
CHANNEL_NAME = CHANNEL_NAME.lower()
SLEEP_TIME = 120
IRC_CHANNEL = "#" + CHANNEL_NAME

#league api key for league commands
try:
    APIKey = sys.argv[3]
except:
    APIKey = ""

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
    global s, HOST, PORT, NICK, CHAN 
    try:
        s.close()
        s.socket.socket()
        s.connect((HOST, PORT))
        s.send(bytes("PASS %s\r\n" % PASS, "UTF-8"))
        s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
        s.send(bytes("JOIN #%s\r\n" % CHAN, "UTF-8"))
        s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
        s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
        s.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
    except:
        print(traceback.format_exc())
#opens channel database or creates new database if one does not already exist
if os.path.exists("{}DB".format(CHAN)):
    dbcon = sqlite3.connect("{}DB".format(CHAN))
    cursor = dbcon.cursor()
else:
    dbcon = sqlite3.connect("{}DB".format(CHAN))
    cursor = dbcon.cursor()
    cursor.execute('CREATE TABLE channelPoints(username text PRIMARY KEY,points INT DEFAULT 0)')
    dbcon.commit()

#globals
duel_list = {} #dictionary used for the duel command
memeteam = ["jereck00", "shin0l", "leo_n_milk"]

def tablereport():
    global dbcon
    global cursor

    for x in cursor.execute('SELECT * from channelPoints ORDER BY points'):
        sendmessage(x)

def requestpoints(message, username):
    global dbcon
    global cursor
    
    messagelist = message.split()
    index = messagelist.index('!points')
    try:
        if len(messagelist) == 1:
            u = username
        elif len(messagelist) == 2:
            u = messagelist[index+1]
        cursor.execute('SELECT points FROM channelPoints WHERE username=?',((u,)))
        sendmessage('{} currently has {} point(s)'.format(username, cursor.fetchone()[0]))
    except:
        print(traceback.format_exc())


def givepoints(username, points):
    global dbcon
    global cursor
    try:
        cursor.execute('UPDATE channelPoints SET points=points+? WHERE username=?',(points, username))
        dbcon.commit()
    except:
        print(traceback.format_exc())


def sendmessage(text):
    # Method for sending a message
    s.send(bytes("PRIVMSG #" + CHAN + " :" + str(text) + "\r\n", "UTF-8"))


def timeout(user, secs):
    timeout_message = "PRIVMSG #" + CHAN + ": /timeout %s %s\r\n" % (user, secs)
    s.send(bytes(timeout_message), "UTF-8")


def uptime():
    global CHAN
    url = "https://api.rtainc.co/twitch/uptime?channel={}".format(CHAN)
    page = requests.get(url)
    for x in page:
        if('is not streaming' not in x.strip().decode('UTF-8')):
            sendmessage("{} has been online for {}".format(CHAN,x.strip().decode('UTF-8')))
        else:
            sendmessage(x.strip().decode('UTF-8'))


def followage(username):
    global CHAN
    url = "https://api.rtainc.co/twitch/channels/{}/followers/{}".format(CHAN,username)
    page = requests.get(url)
    for x in page:
        sendmessage(x.decode('UTF-8'))


def puppet():
    try:
        while True:
            message = input(' assuming direct control: ') 
            sendmessage(message)
            commands(message, 'ardahBot')
    except BrokenPipeError:
        socketconnection()
        
    
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
    duelMessage = '{} has challenged {} to a duel PogChamp type !accept to confirm duel'.format(challenger, target)
    sendmessage(duelMessage)


def cointoss(username):
    global duel_list
    coin = random.randint(0, 1)
    if coin == 0:
        victory_message = '{} has won the duel against {}! PogChamp'.format(username, duel_list[username])
        sendmessage(victory_message)
    if coin == 1:
        defeat_message = '{} has defeated {} in a duel! PogChamp'.format(duel_list[username], username)
        sendmessage(defeat_message)

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

    if message == "!corn" and username in memeteam:
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
            time.sleep(2)
            sendmessage('!accept')
            time.sleep(2)
            cointoss('ardahbot')

    if message == '!accept' and username in duel_list:
        time.sleep((random.randint(0,1)))
        cointoss(username) 

    if message == '!decline' and username in duel_list:
        decline_message = '{} has declined the duel with {}'.format(username, duel_list[username])
        sendmessage(decline_message)
        del duel_list[username]
        
    if message == '!clearduels' and username in memeteam:
        duel_list = {} 
        sendmessage('clearing duel list')

    if message == '!n8iscool' and username in memeteam:
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
        summonerName = message.replace('!lookup', '').replace(' ', '')
        try:
            responseJSON  = requestSummonerData(region, summonerName, APIKey)
            ID = responseJSON[summonerName]['id']
        except KeyError:
            sendmessage("The summoner name {} does not exist".format(summonerName))
            print(traceback.format_exc())
        try:
            ID = str(ID) 
            responseJSON2 = requestRankedData(region, ID, APIKey)
            rank = responseJSON2[ID][0]['tier']
            rank += " %s" % responseJSON2[ID][0]['entries'][0]['division']
            sendmessage("Summoner {} is rank {}, {} LP".format(summonerName, rank, responseJSON2[ID][0]['entries'][0]['leaguePoints']))
        except:
            sendmessage("The summoner {} currently has no ranking".format(summonerName))
            print(traceback.format_exc())

    if '!test' in message and username == 'jereck00':
        tablereport() 

    if '!points' in message and username == 'jereck00':
        requestpoints(message, username)

    if '!givepoints' in message and username == 'jereck00':
        messagelist = message.split()
        index = messagelist.index('!givepoints')
        u = str(messagelist[index+1]) #username
        p = messagelist[index+2] #points
        givepoints(u,p)

    if message == '!uptime':
        uptime()

    if message == '!followage':
        followage(username)

#sendmessage('HeyGuys')
t = threading.Thread(target=puppet).start()

def messageloop():
    while True:
        global s, readbuffer, dbcon, cursor
        
        try:
            readbuffer = readbuffer+s.recv(1024).decode("UTF-8") 
        except KeyboardInterrupt:
            raise
        except:
           print(traceback.format_exc())   
        
        temp = str.split(readbuffer, "\r\n")
#temp = [ str(e.encode('UTF-8')).rstrip() for e in temp ]
        readbuffer = temp.pop()
               
        for line in temp:
            if(line[0] == "PING"):
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
            else:
                parts = str.split(line, ":")

                try:
                    message = parts[2][:len(parts[2])]
                    
                except:
                    message = ""

                usernamesplit = str.split(parts[1], "!")
                username = usernamesplit[0]

                cursor.execute('INSERT OR IGNORE INTO channelPoints (username, points) VALUES (?,?)',(username,'0'))
                givepoints(username, 1)
                dbcon.commit()
                
                print(username + ": " + message)
                commands(message.lower(), username.lower())

while True:
    try:
        messageloop()
    except KeyboardInterrupt:
        raise 
    except:
        print(traceback.format_exc())
        socketconnection()
        messageloop()
