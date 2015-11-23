import socket, string, time

 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "ardahbot"
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
 
# Method for sending a message
def Send_message(message):
    s.send("PRIVMSG #jereck00 :" + message + "\r\n")
 
 
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
                    
                    if message.find("lmao") != -1:
                        Send_message("EleGiggle")
                        
                    if message == "!sliced":
                        Send_message("**unsheeths katana**")
                        
                    if message == "!time":
                        Send_message (time.ctime())

                    if message == "!whoami":
                        Send_message (username)

                   """
                    if message == "!vote":
                        option1=0
                        option2=0
                        #startTime = time.timegm()
                        Send_message("Voting enabled")
                        while username=="jereck00" and message!="!stopvote":
                            if message == "1":
                                option1 += 1
                            if message == "2":
                                option2 += 1
                        if option1 > option2:
                            Send_message("Option 1 wins")
                        if option2 > option1:
                            Send_message("Option 2 wins")
                      """
#################################################################
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
