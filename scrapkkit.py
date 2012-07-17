#!/usr/bin/python
# Scrapkkit IRC Bot [https://www.github.com/resba/Scrapkkit]
# Built off of Sprokkit v0.1 [https://www.github.com/resba/Sprokkit]
# Script by Resba
# Version: 0.0.1-ALPHA
# 
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# 
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.

# Step 1: Import all the necessary libraries.
import socket, sys, string, time, mongokit, random, re
from mongokit import Document, Connection
import settings

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' 0 * :SprokkitBot\r\n' )
global nameslist
global sentmessage
global messageable
#global blacklist
messageable = ''
#blacklist = ''
lastUsed = time.time()
# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""

    def filterResponse():
        sentmessage = data
        if (debug == 1):
            woot.send ( 'PRIVMSG '+channel+' :Loaded filterResponse Function with '+sentmessage+' as the trigger. \r\n' )
        #The command has been called. First check to see what type of command was called.
        if data.find ( ':!' ) != -1:
            global messageable 
            chanstart = data.rsplit('PRIVMSG ')
            chan2 = chanstart[1].rsplit(' :')
            messageable = chan2[0]
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :The command was an announement ! \r\n' )
            #The command was an announcement. now we check for privilages.
            mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :Last Message: %s\r\n'%mySubString )
            atsymbol = "@"
            voicesymbol = "+"
            #If the nameslist variable contains the user with some sort of privilage. The check ends and returns to the command.
            if nameslist.find(atsymbol+mySubString) != -1:           
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are an op \r\n' )
                #because this is a global filter, the messageable is named the channel because its an announcement.
                return 0
            elif nameslist.find(voicesymbol+mySubString) != -1:
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are voiced \r\n' )
                return 0
            else:
                #If the user is NOT privilidged, then they need to jump through a few more hoops.
                mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
                if(debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are not an elevated user \r\n' )
 #               if (mySubString == blacklist):
 #                   return 1
                if(time.time() - lastUsed) > 10:
                    global lastUsed
                    lastUsed = time.time()
                    if (debug == 1):
                        woot.send ('PRIVMSG '+channel+' :lastUsed Check Passed, now returning to command \r\n' )
                    return 0
                else:
                    if (debug == 1):
                        woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
                    return 1
        elif data.find ( ':^' ) != -1:
            #The Command was a Privmsg, so we send the privmsg.
            global readUserName
            readUserName = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            global messageable 
            messageable = readUserName
            return 0
# Feelin' up the channel.
    from commands import base
    try:
    
    from commands import quote
    
    except IndexError:
        woot.send( 'PRIVMSG '+messageable+' :Error! That is not a valid number! \r\n' )
    except ValueError:
        woot.send( 'PRIVMSG '+messageable+' :Error! That is not a valid number! \r\n' )
    except sre_constants.error:
        woot.send( 'PRIVMSG '+messageable+' :Error! You have entered bad regex. Please Try Again. \r\n' )
    
#    except TypeError:
#        woot.send( 'PRIVMSG '+messageable+' :Sorry man, I got nothin! :( \r\n' )
#    if data.find ( 'test' ) != -1:
#        if (filterResponse() == 0):
#            woot.send( 'PRIVMSG '+messageable+' :Test command \r\n' ) 
    if data.find ( 'version' ) != -1:
        if (filterResponse() == 0):
            woot.send( 'PRIVMSG '+messageable+' :--[Ivanna IRC Bot]-- a pure python IRC bot by resba. v1.2-rave https://www.github.com/resba/Scrapkkit \r\n' )

    from commands import debug
