import socket, string, random, twitch, time
from collections import deque
 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "ardahbot"
CHAN = 'jereck00'
PORT = 6667
PASS = "oauth:3hfhwlewgv2ydwkhohs6udttriheuo"
readbuffer = ""
MODT = False
 
# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #jereck00 \r\n")

#garbage vars bc im garbage at python
duel_list = deque([])
defender = ''
duel_check = False

def sendmessage(text):
# Method for sending a message
    s.send("PRIVMSG #jereck00 :" + text + "\r\n")

def timeout(user, secs):
    timeout_message = "PRIVMSG #jereck00 :/timeout %s %s\r\n" % (user, secs)
    s.send(timeout_message)

def tofile(text,username):
    username = str(username)
    text = str(text)
    with open('test.txt', 'a') as textfile:
        print 'writing to file'
        textfile.write(username + ':' + text + '\r\n')
        textfile.close()

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

                    if 'tmi.twitch.tv' not in message:
                        tofile(message, username)

                    if message == "!meme":
                        sendmessage("EleGiggle")
                        
                    if message == "!sliced":
                        sendmessage("**unsheathes katana**")

                    if message == "!whoami":
                        sendmessage(username)

                    if message == "!corn":
                        sendmessage("https://33.media.tumblr.com/b07644c8da2e4b15c6119d37078d2e16/tumblr_n6kja1gWkE1qln00mo2_400.gif")

                    if message == "!hotdog":
                        sendmessage("Kreygasm")

                    if message == "!sudoku":
                        kick_message = ('kicking %s from chat') % (username)
                        print(kick_message)
                        sendmessage("He will be missed...")
                        timeout(username, 15)

                    if '!duel' in message and len(duel_list) == 0:
                        duel_list.append(username)
                        duel_list.append(message[6:])
                        duel_message = '/me %s has challenged %s to a duel PogChamp type !accept to confirm duel' % (duel_list[0], duel_list[1])
                        sendmessage(duel_message)

                    if len(duel_list) == 2 and username == duel_list[1] and message == '!accept':
                        coin = random.randint(0, 1)
                        if coin == 0:
                            victory_message = '/me %s has won the duel against %s! PogChamp' % (duel_list[0], duel_list[1])
                            sendmessage(victory_message)
                        if coin == 1:
                            defeat_message = '/me %s has defeated %s in a duel! PogChamp' % (duel_list[1], duel_list[0])
                            sendmessage(defeat_message)
                            sendmessage('Never lucky BabyRage')
                        duel_list.popleft()
                        duel_list.popleft()
                        #TODO take this len() check out after implementing better queue system
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
                            victory_message = '/me %s has won the duel against %s! PogChamp' % (duel_list[0], duel_list[1])
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
                        sendmessage('https://38.media.tumblr.com/1f1ea822c3b32719c382d775c629713a/tumblr_mwzoseIvD01sedjuto1_500.gif')
                        
                    if message == '!hotdogs' and username == 'n8many':
                        n8_hotdog_game_message = 'looks like n8 wants some hotdogs...' 
                        sendmessage(n8_hotdog_game_message)
                        sendmessage('8=D')
                        def anotherdoodle():
                            from time import sleep
                            sleep(0.4)
                            doodleyes = random.randint(1,4)
                            if doodleyes == 1:
                                sendmessage('no more doodle for n8 lmao')
                            else:
                                sendmessage('8=D')
                                anotherdoodle()
                        anotherdoodle()    
                        
                    if message == '!hotdogs' and username != 'n8many':
                        hotdog_game_message = 'looks like %s is playing the hotdog game, how many dogs will they get?' % username
                        sendmessage(hotdog_game_message)
                        sendmessage('=(~~~)=')
                        def anotherdog():
                            from time import sleep
                            sleep(0.4)
                            hotdogyes = random.randint(1,4)
                            if hotdogyes == 1:
                                sendmessage('no more dogs')
                            else:
                                sendmessage('=(~~~)=')
                                anotherdog()
                        anotherdog()

#################################################################
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
