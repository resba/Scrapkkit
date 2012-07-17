#!/usr/bin/python
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