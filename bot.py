import socket
import string
import random
import time
import urllib2
import json
import threading
import os
import traceback
import sys
from collections import deque

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv" #irc.twitch.tv
NICK = "ardahbot"
CHAN = 'jereck00'
PORT = 6667
PASS = "oauth:3hfhwlewgv2ydwkhohs6udttriheuo"
readbuffer = ""
MODT = False

CHANNEL_NAME = "jereck00"
CHANNEL_NAME = CHANNEL_NAME.lower()
SLEEP_TIME = 120
IRC_CHANNEL = "#" + CHANNEL_NAME

HOST2 = "199.9.253.119"

followsMap = {}
modsMap = {}
points = {}

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s2 = socket.socket()
s.connect((HOST, PORT))
s2.connect((HOST2, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #jereck00 \r\n")
s.send("CAP REQ :twitch.tv/membership\r\n")
s.send("CAP REQ :twitch.tv/commands\r\n")
s.send("CAP REQ :twitch.tv/tags\r\n")

s2.send("PASS " + PASS + "\r\n")
s2.send("NICK " + NICK + "\r\n")
s2.send("JOIN #_ardahbot_1454310601454\r\n")
s2.send("CAP REQ :twitch.tv/membership\r\n")
s2.send("CAP REQ :twitch.tv/commands\r\n")
s2.send("CAP REQ :twitch.tv/tags\r\n")


# garbage vars bc im garbage at python
duel_list = deque([])
defender = ''
duel_check = False

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
        r = urllib2.urlopen('http://tmi.twitch.tv/group/user/' + CHANNEL_NAME + "/chatters")
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
        print "User: " + user
        print "Message: " + ' '.join(msg)
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
                print "subtracting "
                if msg[2] in points:
                    points[msg[2]] = points[msg[2]] - int(msg[3])
                else:
                    points[msg[2]] = int(msg[3])
    except:
        print traceback.format_exc()


def sendmessage(text):
    # Method for sending a message
    s.send("PRIVMSG #jereck00 :" + text + "\r\n")


def sendSecret(username):
    s2.send("PRIVMSG #ardahBot :.w " + username + " nice\r\n")


def timeout(user, secs):
    timeout_message = "PRIVMSG #jereck00 :/timeout %s %s\r\n" % (user, secs)
    s.send(timeout_message)

def generatememe(fill="XX", empty="__", height=8, width=8, fillpercent=0.4):
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



sendmessage('it that bot')


while True:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        else:
            # Splits the given string so we can work with it better
            parts = string.split(line, ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                if MODT:
                    print username + ": " + message

                    ########################### Commands #############################

                    t = threading.Thread(target=addPoints).start()

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
                        print 'kicking %s from chat' % username
                        sendmessage("He will be missed...")
                        timeout_message = "PRIVMSG #jereck00 :/timeout %s %s\r\n" % (username, 30)
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
                        # TODO take this len() check out after implementing better queue system
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

                    if message == '!nice' and username == 'leo_n_milk':
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

                    if message == '!meme_me':
                        generatememe()

                    #################################################################
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
