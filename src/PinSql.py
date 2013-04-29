import math
import time
import pprint
import urllib2
import re
import sys
from bs4 import BeautifulSoup
from unicoderw import UnicodeWriter
import pymysql 


searchword="fashion"
pinurl = "http://pinterest.com"
boardpgurl = "http://pinterest.com/search/boards/?q="+searchword+"&page="

#keywords = ['fashion','style','cloth','closet','outfit','apparel']


# Get initial boards from search
def getinitial():
    nboardpages=2
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
                # get users
                for username_a in board_div.find_all("a","colorless"):
                    username = username_a["href"]
                    cur.execute("SELECT COUNT(1) FROM Users WHERE username=\"%s\"" % (username))
                    if cur.fetchone()[0]!=1:
                        try:
                            cur.execute("INSERT INTO Users(username) VALUES (\"%s\")" % (username))
                        except:
                            print "Error inserting user:\n%s" % (username)
                        else:
                            user=cur.execute("SELECT LAST_INSERT_ID()")
                            userid=str(cur.fetchone()[0])
                    else:
                        print "User exists"
                        cur.execute("SELECT userid FROM Users WHERE username=\"%s\"" % (username))
                        userid=str(cur.fetchone()[0])
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
                                cur.execute("SELECT boardid FROM Boards WHERE boardname=\"%s\"" % (board_name))
                                boardid=str(cur.fetchone()[0])
                                cur.execute("INSERT INTO user_has_boards(user_userid,boards_boardid) VALUES (\"%s\",\"%s\")" % (userid,boardid))
                        else:
                            print "Board exists"

    conn.commit()
    
   
    cur.execute("SELECT COUNT(*) FROM Boards")
    number=cur.fetchone()[0]
    print "Number of initial boards: "+str(number)
    return True
    

if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()


    
    boardlist = getinitial()
    
    
    

