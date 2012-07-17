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

import socket, sys, string, time, mongokit, random, re
from mongokit import Connection
import models

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

debug = 0

connection = Connection(mongo_host,mongo_port)

connection.register([Quote])