import math
import time
import pprint
import urllib2
import re
import sys
from bs4 import BeautifulSoup
import pymysql 


searchword="fashion"
pinurl = "http://pinterest.com"
boardpgurl = "http://pinterest.com/search/boards/?q="+searchword+"&page="

keywords = ['fashion','style','cloth','closet','outfit','apparel']


# Get initial boards from search
def getinitial():
    cur.execute("TRUNCATE Boards")
    cur.execute("TRUNCATE Pins")
    cur.execute("TRUNCATE Sources")
    cur.execute("TRUNCATE Board_has_pins")
    cur.execute("TRUNCATE Pin_has_sources")
    conn.commit()
    nboardpages=1
    for bpage in range(1,nboardpages+1):
        print "opening board list " + str(bpage)

        # test whether more than 0.5 second has passed
        start=time.time()
        elapsed = time.time() - start
        if elapsed > 0.5:
            time.sleep(0.5)
        start = time.time()

        # try to open search page
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            boardpg = opener.open(boardpgurl+str(bpage))
        except IOError, e:
           if hasattr(e, 'reason'):
               print 'We failed to reach a server.'
               print 'Reason: ', e.reason
           elif hasattr(e, 'code'):
               print 'The server couldn\'t fulfill the request.'
               print 'Error code: ', e.code
        else:
            boardread = boardpg.read()
            soup = BeautifulSoup(boardread)
            #print soup
            for board_div in soup.find_all("div","pin pinBoard"):
                # get boards
                for h3_name in board_div("h3","serif"):
                    for a_name in h3_name("a"):
                        board_name=a_name['href']
                        cur.execute("SELECT COUNT(1) FROM Boards WHERE boardname=\"%s\"" % (board_name))
                        if cur.fetchone()[0]!=1:
                            try:
                                cur.execute("INSERT INTO Boards(boardname) VALUES (\"%s\")" % (board_name))
                            except:
                                print "Error inserting board:\n%s" % (board_name)
                        else:
                            print "Board exists"

    conn.commit()
    
   
    #cur.execute("SELECT COUNT(*) FROM Boards")
    #number=cur.fetchone()[0]
    #print "Number of initial boards: "+str(number)
    return True

# get pins from boards
def getpins():
    sqlboards="SELECT boardname FROM Boards WHERE is_crawled='0'"
    cur.execute(sqlboards)
    boards=cur.fetchall()
    for item in boards:
        #print str(item[0])
        cur.execute("SELECT boardid FROM Boards WHERE boardname=\"%s\"" % str(item[0]))
        board_id=str(cur.fetchone()[0])
        print "Crawling board id=" + board_id
        
        # test whether more than 0.5 second has passed
        start=time.time()
        elapsed = time.time() - start
        if elapsed > 0.5:
            time.sleep(0.5)
        start = time.time()

        # open pins in board
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            firstpg = opener.open(pinurl + str(item[0]))
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            pageread = firstpg.read()
            count = re.compile(ur'<strong>(.*?)</strong> pins', re.UNICODE)
            pincount_group = count.search(pageread)

            # if error opening page, try again
            if not pincount_group:
                continue
            pincount = pincount_group.group(1)
            npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)

            print "Pin pages in board "+": "+str(npages)
            npage=int(npages)
            for i in range(1,npage+2):

                # test whether more than 0.5 second has passed
                start=time.time()
                elapsed = time.time() - start
                if elapsed > 0.5:
                    time.sleep(0.5)
                start = time.time()

                # open pin page i
                try:
                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    pages=opener.open(pinurl + str(item[0])+"?page="+str(i))
                except IOError, e:
                    if hasattr(e, 'reason'):
                        print 'We failed to reach a server.'
                        print 'Reason: ', e.reason
                    elif hasattr(e, 'code'):
                        print 'The server couldn\'t fulfill the request.'
                        print 'Error code: ', e.code
                else:
                    # test whether more than 0.1 second has passed
                    elapsed = time.time() - start
                    if elapsed > 0.1:
                        time.sleep(0.1)
                    start = time.time()
                    page=pages.read()
                    soup = BeautifulSoup(page)                 
                    for pin in soup.find_all("div","pin"):
                        pinid = "None"
                        board = "None"
                        source = "None"
                        userid = "None"
                        for pinid_a in pin.find_all("a","PinImage ImgLink"):
                            pinid = pinid_a['href']
                            #print pinid
                            cur.execute("SELECT COUNT(1) FROM Pins WHERE pinnum=\"%s\"" % (pinid))
                            if cur.fetchone()[0]!=1:
                                try:
                                    cur.execute("INSERT INTO Pins(pinnum) VALUES (\"%s\")" % (pinid))
                                    cur.execute("SELECT LAST_INSERT_ID()")
                                    pin_id=str(cur.fetchone()[0])
                                    cur.execute("INSERT INTO Board_has_pins(boards_boardid,Pins_pinid) VALUES (\"%s\",\"%s\")" % (board_id,pin_id))
                                except:
                                    print "Error inserting pins:\n%s" % (pinid)
                            else:
                                cur.execute("SELECT pinid FROM Pins WHERE pinnum=\"%s\"" % (pinid))
                                pin_id=str(cur.fetchone()[0])
                                cur.execute("INSERT INTO Board_has_pins(boards_boardid,Pins_pinid) VALUES (\"%s\",\"%s\")" % (board_id,pin_id))             
                            
                            for clearfix in pin.find_all("div","convo attribution clearfix"):
                                for link in clearfix.find_all("a"):
                                    source = link['href']
                                    cur.execute("SELECT COUNT(1) FROM Sources WHERE sourcename=\"%s\"" % (source))
                                    if cur.fetchone()[0]!=1:
                                        try:
                                            cur.execute("INSERT INTO Sources(sourcename) VALUES (\"%s\")" % (source))
                                            cur.execute("SELECT LAST_INSERT_ID()")
                                            source_id=str(cur.fetchone()[0])
                                            cur.execute("INSERT INTO Pin_has_sources(Pins_pinid,Sources_sourceid) VALUES (\"%s\",\"%s\")" % (pin_id,source_id))
                                        except:
                                            print "Error inserting sources:\n%s" % (source)
                                    else:
                                        cur.execute("SELECT sourceid FROM Sources WHERE sourcename=\"%s\"" % (source))
                                        source_id=str(cur.fetchone()[0])
                                        cur.execute("INSERT INTO Pin_has_sources(Pins_pinid,Sources_sourceid) VALUES (\"%s\",\"%s\")" % (pin_id,source_id))

        cur.execute("UPDATE Boards SET is_crawled='1' WHERE boardid=\"%s\"" % (board_id))
        conn.commit()
    conn.commit()
    return True

# Get Boards from Pins
def getboards():
    newboardlist=[]
    sqlpins="SELECT pinnum FROM Pins WHERE is_crawled='0'"
    cur.execute(sqlpins)
    pins=cur.fetchall()
    for item in pins:
        #print str(item[0])
        cur.execute("SELECT pinid FROM Pins WHERE pinnum=\"%s\"" % str(item[0]))
        pin_id=str(cur.fetchone()[0])
        #print pin_id
    
        # test whether more than 0.5 second has passed
        start=time.time()
        elapsed = time.time() - start
        if elapsed > 0.5:
            time.sleep(0.5)
        start = time.time()
        
        # open pin page to get list of pinned boards
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            pinpages=opener.open(pinurl+str(item[0]))
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            pinpage=pinpages.read()
            soup=BeautifulSoup(pinpage)
            for spin in soup.find_all("span","repin_post_attr"):
                # remove http://pinterest.com
                fullboardname = spin.a.next_sibling.next_sibling['href']
                newboardname = fullboardname[len("http://pinterest.com"):]
                #print newboardname
                # check if keywords in newboardname
                for c in keywords:
                    if c in newboardname:
            		#check if newboard is in Boards Table
                        cur.execute("SELECT COUNT(1) FROM Boards WHERE boardname=\"%s\" AND is_crawled=0" % (newboardname))
                        if cur.fetchone()[0]!=1:
                            try:
                                cur.execute("INSERT INTO Boards(boardname) VALUES (\"%s\")" % (newboardname))
                                print "New Board added"
                            except:
                                print "Error inserting board:\n%s" % (newboardname)  

        cur.execute("UPDATE Pins SET is_crawled='1' WHERE pinid=\"%s\"" % (pin_id))
        conn.commit()
    conn.commit()
    return True

if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()
    restart = True
    
    if restart:
        print "Getting initial boards from search"
        boardlist=getinitial()
        
        print "Getting pins from initial boards"
        pins = getpins()
        
        print "Getting new boards from pins"
        newboards=getboards()
        
    

    for z in range(0,1):
        
        print "Getting pins from boards"
        pins=getpins()
        print "Getting new boards from pins"
        newboards=getboards()
        
    cur.close()
    conn.close()

    


