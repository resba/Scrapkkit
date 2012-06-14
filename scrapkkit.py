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


# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
host = raw_input('Enter Host: ')
channel = raw_input('Enter Channel: ')
port = 6667
nick = "Ivanna"
#host = 'irc.eu.esper.net'
name =  "resbabot"
#channel = '#bukkit+++'
ident = 'resbabot'
#Nickpasscheck: 1 - The nick requires a pass. 0 - The nick does NOT require a pass.
nickpasscheck = 0
#Nickpass: Password for Nick (If required.)
nickpass = 'changeme'

#botadmin: your nick is inputted for access to debug commands such as graceful shutdown and debug messages
botadmin = 'resba'
botadmin2 = 'pronto'

mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db = 'ircq'

connection = Connection(mongo_host,mongo_port)

class Quote(Document):
    use_schemaless = True
    structure = {
        'uid': int,
        'quote': str,
    }
    use_dot_notation = True

connection.register([Quote])

#DebugSwitch: For use when debug is needed.
debug = 0

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
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
        if (debug == 1):
            woot.send( 'PRIVMSG '+channel+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n');
    if (nickpasscheck == 1):
        if data.find ( 'NickServ!' ) != -1:
            woot.send ( 'PRIVMSG NickServ :IDENTIFY '+nick+' '+nickpass+'\r\n' )
            nickpasscheck = 0
    try:
        if data.find ( 'plusq' ) != -1:
            if (filterResponse() == 0):
                sub = data.rsplit('!plusq ')
                defcol = connection[mongo_db]['quotes']
                fieldlist = list(defcol.Quote.find())
                quote = defcol.Quote()
                quote['uid'] = len(fieldlist)+1
                qid = str(quote['uid'])
                quote['quote'] = sub[1]
                quote.save()
                woot.send( 'PRIVMSG '+messageable+' :Saved quote '+qid+' to database. \r\n' )

        if data.find( 'indexq' ) != -1:
            if (filterResponse() == 0):
                sub = data.rsplit('!indexq ')
                defcol = connection[mongo_db]['quotes']
                fieldlist = defcol.Quote.find_one({'uid': int(sub[1])})
                farray = [fieldlist]
                fint = [x['uid'] for x in farray]
                fquote = [x['quote'] for x in farray]
                final = fquote[0].replace('\r\n','')
                qid = str(len(list(defcol.Quote.find())))
                woot.send( 'PRIVMSG '+messageable+' :Quote ['+str(fint[0])+'/'+str(qid)+'] -- '+str(final)+' \r\n' )
        if data.find( 'findq' ) != -1:
            if (filterResponse() == 0):
                if (debug == 1):
                    woot.send ('PRIVMSG '+messageable+' :I started the command. \r\n')
                sub = data.rsplit('!findq ')
                defcol = connection[mongo_db]['quotes']
                fieldlist = list(defcol.Quote.find())
                fquote = [x['quote'] for x in fieldlist]
                param = sub[1]
                results = []
                inte = 0
                pattern = re.compile(param)
                while inte != len(fquote):
                    if pattern.search(str(fquote[inte])) != None :
                        results.append(str(fquote[inte]))
                    inte = inte + 1
                if(len(results)==0):
                    woot.send( 'PRIVMSG '+messageable+' :Count -- ' + str(len(results)) + '\r\n')
                    woot.send( 'PRIVMSG '+messageable+' :Sorry, no results. \r\n' )
                elif(len(results) == 1):
                    woot.send( 'PRIVMSG '+messageable+' :Found 1 Quote!. \r\n' )
                    woot.send( 'PRIVMSG '+messageable+' :'+results[0]+'. \r\n' )
                elif(len(results) > 1):
                    woot.send( 'PRIVMSG '+messageable+' :Found '+str(len(results))+' Quotes! Picking one at Random \r\n' )
                    woot.send( 'PRIVMSG '+messageable+' :'+results[random.randint(0,int(len(results)))]+' \r\n' )
#                    if(fieldlist.count() > 1):
#                        woot.send( 'PRIVMSG '+messageable+' :More than 1 match \r\n')
#                    elif(fieldlist.count() == 1):
#                        woot.send ('PRIVMSG '+messageable+' :SUCCESS! \r\n')
            if (debug == 1):
                woot.send ('PRIVMSG '+messageable+' :I got to the end of the command. \r\n')
#        if data.find( 'findq' ) != -1:
#            if (filterResponse() == 0):
#                sub = data.rsplit('!findq ')
#                defcol = connection[mongo_db]['quotes']
#                fieldlist = defcol.Quote.find_one({'quote': { '$regex' : str(sub[1]), '$options': 'i' }})
#                #farray = fieldlist
#                #fint = [x['uid'] for x in farray]
#                #fquote = [x['quote'] for x in farray]
#                #final = fquote[0].replace('\r\n','')
#                qid = str(len(list(defcol.Quote.find())))
#                woot.send( 'PRIVMSG '+messageable+' :Quote ['+str(fieldlist['uid'])+'/'+str(qid)+'] -- '+str(fieldlist['quote'])+' \r\n' )
        if data.find( 'randq' ) != -1:
            if (filterResponse() == 0):
                defcol = connection[mongo_db]['quotes']
                qid = str(len(list(defcol.Quote.find())))
                fieldlist = defcol.Quote.find_one({'uid': random.randint(0,int(qid))})
                farray = [fieldlist]
                fint = [x['uid'] for x in farray]
                fquote = [x['quote'] for x in farray]
                final = fquote[0].replace('\r\n','')
                woot.send( 'PRIVMSG '+messageable+' :Quote ['+str(fint[0])+'/'+str(qid)+'] -- '+str(final)+' \r\n' )


##TODO: Random Quote

    except IndexError:
        woot.send( 'PRIVMSG '+messageable+' :Error! That is not a valid number! \r\n' )
    except ValueError:
        woot.send( 'PRIVMSG '+messageable+' :Error! That is not a valid number! \r\n' )
    except sre_constants.error:
        woot.send( 'PRIVMSG '+messageable+' :Error! You have entered bad regex. Please Try Again. \r\n' )
    
#    except TypeError:
#        woot.send( 'PRIVMSG '+messageable+' :Sorry man, I got nothin! :( \r\n' )
    if data.find ( 'test' ) != -1:
        if (filterResponse() == 0):
            woot.send( 'PRIVMSG '+messageable+' :Test command \r\n' ) 
    if data.find ( 'version' ) != -1:
        if (filterResponse() == 0):
            woot.send( 'PRIVMSG '+messageable+' :--[Ivanna IRC Bot]-- a pure python IRC bot by resba. v1.2-rave https://www.github.com/resba/Scrapkkit \r\n' )

    def debugGrace():
        global messageable
        if (messageable == ''):
            messageable = channel
        if (debug == 1):
            woot.send('PRIVMSG '+messageable+' :debugGrace() has been loaded \r\n' )
        sentmessage = data
        mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
        if (mySubString == botadmin or mySubString == botadmin2):
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 1 \r\n' )
            return 1
        else:
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 0 \r\n' )
            return 0
# Command to gracefully close Wikkit and disconnect it from the
# Server.
    if data.find ( '!debug.timetogo') != -1:
        thenull = ""
        if (debugGrace() == 1):
            woot.send ("QUIT :I have been Deadeded. %s\r\n" % thenull )
            woot.close()
            sys.exit()
#Toggles Debug
    if data.find ( '!debug.debug') != -1:
        if (debugGrace()==1):
            if (debug == 0):
                debug = 1
                woot.send ('PRIVMSG '+messageable+' :Debug is ON \r\n')
            elif (debug == 1):
                debug = 0
                woot.send ('PRIVMSG '+messageable+' :Debug is OFF \r\n')
#Fun debug commands
    if data.find ( '!debug.reloader' ) != -1:
        if (debugGrace()==1):
            woot.send ( 'NAMES '+messageable+' \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Boom! \r\n')
    if data.find ( '!debug.lastUsed') != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % lastUsed )
    if data.find ( '!debug.time.time' ) != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % time.time() )
    if data.find ( '!debug.blacklist' ) != -1:
        if (debugGrace()==1):
            sub = data.rsplit('!debug.blacklist ')
            blacklist = sub[0]
            woot.send ('PRIVMSG '+messageable+' :Got it. \r\n' )

    if data.find ( '!addch' ) != -1:
        if (debugGrace()==1):
            sub = data.rsplit('!addch ')
            woot.send ('JOIN '+sub[1]+'\r\n')
