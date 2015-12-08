import socket, string, random, twitch
 
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
duel_list = []
defender = ''
duel_check = False


# Method for sending a message
def sendmessage(text):
    s.send("PRIVMSG #jereck00 :" + text + "\r\n")

def timeout(user, secs):
    s.send("PRIVMSG #jereck00 :/timeout" + user + str(secs) + "\r\n")

def tofile(text,username):
    username = str(username)
    text = str(text)
    with open('test.txt', 'a') as textfile:
        print 'writing to file'
        textfile.write(username + ':' + text + '\r\n')
        textfile.close()

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
                        duel_list.pop()
                        duel_list.pop()
                        duel_check = False

                    if message == '!cancelduel' and username == duel_list[0] and len(duel_list) == 2:
                        cancel_duel_message = '%s has canceled the duel' % (duel_list[0])
                        sendmessage(cancel_duel_message)
                        defender = ''
                        attacker = ''
                        duel_check = False



#################################################################
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
