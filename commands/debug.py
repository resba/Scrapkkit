#!/usr/bin/python
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