import socket, string, random, time
 
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
defender = ''
duel_check=False


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

def readfile():
    textfile = open('test.txt', 'r+')
    print 'reading from file'
    words = textfile.readline()
    textfile.close()
    return words

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

                    if 'tmi.twitch.tv' or 'tmi.twitch.tv:' not in message:
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
                        sendmessage("He will be missed...")
                        timeout(username, 30)

                    if (message == "!read") and (username == "jereck00"):
                        sendmessage(readfile())

                    if '!duel' in message and duel_check == False:
                        attacker = username
                        defender = message[6:]
                        duel_message = '/me %s has challenged %s to a duel PogChamp type !accept to confirm duel' % (attacker, defender)
                        sendmessage(duel_message)
                        duel_check = True

                    if duel_check == True and username == defender and message == '!accept':
                        coin = random.randint(0,1)
                        if coin == 0:
                            victory_message = '/me %s has won the duel against %s! PogChamp' % (attacker, defender)
                            sendmessage(victory_message)
                        if coin == 1:
                            defeat_message = '/me %s has defeated %s in a duel! PogChamp' % (defender, attacker)
                            sendmessage(defeat_message)
                        defender = ''
                        attacker = ''
                        duel_check = False


#################################################################
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
