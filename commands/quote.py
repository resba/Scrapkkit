#!/usr/bin/python
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

        if data.find ( 'addquote' ) != -1:
            if (filterResponse() == 0):
                sub = data.rsplit('!addquote ')
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