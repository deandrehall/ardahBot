import urllib2
import json
import time
import threading
import socket
import string
import os
import random
import traceback
import sys

# CONFIG
CHANNEL_NAME = "jereck00"
CHANNEL_NAME = CHANNEL_NAME.lower()
SLEEP_TIME = 120
IRC_CHANNEL = "#" + CHANNEL_NAME

host = "irc.twitch.tv"
port = 6667
nick = "ardahbot" + str(random.randint(10000, 9999999))
readbuffer = ""
s = socket.socket()
s.connect((host, port))
s.send("NICK %s\r\n" % nick)
s.send("JOIN %s\r\n" % IRC_CHANNEL)
followsMap = {}
modsMap = {}
points = {}

if os.path.exists("points.txt"):
    pass
else:
    pointsFile = open("points.txt", "w+")
    pointsFile.close()
pointsFile = open("points.txt", "r")
for line in pointsFile:
    line = line.strip()
    line = line.split(':')
    points[line[0]] = int(line[1])
pointsFile.close()


def getUser(line):
    user = ""
    if line[1] == "PRIVMSG":
        user = line[0]
        user = user.split("!")
        user = user[0]
        user = user[1:]
    return user


def getMessage(line):
    line = line[3:]
    line = ' '.join(line)
    return line[1:].split(' ')


def follows(user):
    global CHANNEL_NAME
    if user in followsMap:
        return followsMap[user]
    else:
        try:
            r = urllib2.urlopen("https://api.twitch.tv/kraken/users/" + user + "/follows/channels/" + CHANNEL_NAME + "")
            followJson = json.loads(r.read())
            if "error" in followJson:
                followsMap[user] = False
                return False
            else:
                followsMap[user] = True
                return True
        except:
            return False


def addPoints():
    global CHANNEL_NAME
    while True:
        r = urllib2.urlopen("http://tmi.twitch.tv/group/user/" + CHANNEL_NAME + "/chatters")
        chattersJson = json.loads(r.read())
        for x in range(0, len(chattersJson["chatters"]["moderators"])):
            modsMap[chattersJson["chatters"]["moderators"][x]] = True
        for x in range(0, len(chattersJson["chatters"]["staff"])):
            modsMap[chattersJson["chatters"]["staff"][x]] = True
        for x in range(0, len(chattersJson["chatters"]["admins"])):
            modsMap[chattersJson["chatters"]["admins"][x]] = True
        for x in range(0, len(chattersJson["chatters"]["global_mods"])):
            modsMap[chattersJson["chatters"]["global_mods"][x]] = True

        for x in range(0, len(chattersJson["chatters"]["viewers"])):
            # print "user: " + chattersJson["chatters"]["viewers"][x]
            user = chattersJson["chatters"]["viewers"][x]
            curPoints = 0
            if user in points:
                if follows(user) == True:
                    points[user] = points[user] + 3
                else:
                    points[user] = points[user] + 1
            else:
                points[user] = 1
                pass
            pointsFile = open("points.txt", "r+")
            for key in points:
                pointsFile.write(key + ":" + str(points[key]) + "\n")
            pointsFile.close()
        time.sleep(SLEEP_TIME)


t = threading.Thread(target=addPoints).start()


def parseMessage(line):
    try:
        user = getUser(line)
        msg = getMessage(line)
        if user == "" or user == None or user == "jtv":
            return
        curPoints = 0
        if user in points:
            points[user] = points[user] + 1
        else:
            points[user] = 1
        pointsFile = open("points.txt", "r+")
        for key in points:
            pointsFile.write(key + ":" + str(points[key]) + "\n")
        pointsFile.close()
        print("User: " + user)
        print("Message: " + ' '.join(msg))
        message = ' '.join(msg)
        msg = message.split(' ')
        if (msg[0].lower() == "!points") and (len(msg) == 4) and (user in modsMap):
            if msg[1].lower() == "give":
                if msg[2] in points:
                    points[msg[2]] = points[msg[2]] + int(msg[3])
                else:
                    points[msg[2]] = int(msg[3])
        if (msg[0].lower() == "!points") and (len(msg) == 4) and (user in modsMap):
            if msg[1].lower() == "take":
                print("subtracting ")
                if msg[2] in points:
                    points[msg[2]] = points[msg[2]] - int(msg[3])
                else:
                    points[msg[2]] = int(msg[3])
    except:
        print(traceback.format_exc())


while True:
    try:
        readbuffer = readbuffer + s.recv(1024)
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()

        for line in temp:
            line = string.rstrip(line)
            line = string.split(line)
            if len(line) > 3:
                parseMessage(line)
            if (line[0] == "PING"):
                s.send("PONG %s\r\n" % line[1])
    except:
        print(traceback.format_exc())
