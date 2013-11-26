
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import urllib2
import math
import re
import pprint
import pymysql

mainurl="http://www.pinterest.com"


def getinfo(pinnum,pinid):
    driver = webdriver.Firefox()
    driver.get(mainurl+pinnum)
    aarr=[]
    pageread=driver.page_source
    soup=BeautifulSoup(pageread)
    #print soup
    for div in soup.findAll("div","repinLike"):
        for span in div.findAll("span","buttonText"):
            #print span.text
            aarr.append(span.text)
##    for div in soup.findAll("div","boardHeader"):
##        for a in div.findAll("a"):
##            boardowner=a['href']

    # Get Board of the Pin
    for div in soup.findAll("div","closeupBottomView boardCredit Board Module"):
        for a in div.findAll("a","boardLink"):
            boardowner=a['href']
    # Insert Board to db and Update Pin
    cur.execute("SELECT COUNT(1) FROM Boards WHERE Boardname=\"%s\"" % (boardowner))
    if cur.fetchone()[0]!=1:
        try:
            cur.execute("INSERT INTO Boards(Boardname) VALUES (\"%s\")" % (boardowner))
            cur.execute("SELECT LAST_INSERT_ID()")
            boardid=str(cur.fetchone()[0])
            cur.execute("SELECT Boards_boardid FROM Pins WHERE Pinid=\"%i\"" % (int(pinid)))
            if cur.fetchone()[0]!="0":
                cur.execute("UPDATE Pins SET Boards_Boardid=\"%i\" WHERE Pinid=\"%i\"" % (int(boardid),int(pinid)))
        except:
            print "Error inserting board:\n%s" % (boardowner)
    else:
        print "Board exists"
        cur.execute("SELECT boardid FROM Boards WHERE Boardname=\"%s\"" % (boardowner))
        boardid=str(cur.fetchone()[0])
        cur.execute("SELECT Boards_boardid FROM Pins WHERE Pinid=\"%i\"" % (int(pinid)))
        if cur.fetchone()[0]!="0":
            cur.execute("UPDATE Pins SET Boards_Boardid=\"%i\" WHERE Pinid=\"%i\"" % (int(boardid),int(pinid)))
        
    print "BoardID ----" + str(boardid)

    # Get Source of the Pin  
    for div in soup.findAll("div","PaddedPin Module"):
        for a in div.findAll("a"):
            source=a['href']
    # Insert Source to db and Update Pin
    cur.execute("SELECT COUNT(1) FROM Sources WHERE Sourcename=\"%s\"" % (source))
    if cur.fetchone()[0]!=1:
        try:
            cur.execute("INSERT INTO Sources(Sourcename) VALUES (\"%s\")" % (source))
            cur.execute("SELECT LAST_INSERT_ID()")
            sourceid=str(cur.fetchone()[0])
            cur.execute("SELECT Sources_Sourceid FROM Pins WHERE Pinid=\"%i\"" % (int(pinid)))
            if cur.fetchone()[0]!="0":
                cur.execute("UPDATE Pins SET Sources_Sourceid=\"%i\" WHERE Pinid=\"%i\"" % (int(sourceid),int(pinid)))
        except:
            print "Error inserting source:\n%s" % (source)
    else:
        print "Source exists"
        cur.execute("SELECT Sourceid FROM Sources WHERE Sourcename=\"%s\"" % (source))
        sourceid=str(cur.fetchone()[0])
        cur.execute("SELECT Sources_Sourceid FROM Pins WHERE Pinid=\"%i\"" % (int(pinid)))
        if cur.fetchone()[0]!="0":
            cur.execute("UPDATE Pins SET Sources_Sourceid=\"%i\" WHERE Pinid=\"%i\"" % (int(sourceid),int(pinid)))
    conn.commit()

    print aarr
    if aarr[1]=="Like":
        pincount=int(aarr[0])
    else:
        pincount=0
        
    print "Boardowner: " + boardowner + " pin has " + str(pincount) + " repin(s)"
    print "Pin source: " + source
    driver.close()

    # Get repins
    if pincount !=0:
        driver = webdriver.Firefox()
        driver.get(mainurl+pinnum+"repins/")
        pins=[]
        b=0

        while True:
            prelen=len(pins)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.5)

            html = driver.page_source
            soup = BeautifulSoup(html)
            i=0
            for a in soup.findAll("a","boardLinkWrapper"):
                i+=1
                #print i
                boardid=a['href']
                if boardid not in pins:
                    pins.append(boardid)

            #print len(pins)
            #print i
 
            if prelen==len(pins):
                #print "Ayni"
                b+=1
                if b>10:
                    break
            else:
                b=0
                #print "Farkli"
            prelen=len(pins)
            if len(pins) >=pincount:
                break
      
    ##    #pprint.pprint(pins)
        print str(len(pins)) + " repins found"
        
        # Insert repins to db
        for i in range(0,len(pins)):
             cur.execute("SELECT COUNT(1) FROM Boards WHERE Boardname=\"%s\"" % (pins[i]))
             if cur.fetchone()[0]!=1:
                try:
                    cur.execute("INSERT INTO Boards(Boardname) VALUES (\"%s\")" % (pins[i]))
                    cur.execute("SELECT LAST_INSERT_ID()")
                    repinboardid=str(cur.fetchone()[0])
 
                    cur.execute("INSERT INTO Pin_has_repinboards(Pins_Pinid,Boards_Boardid) VALUES (\"%i\",\"%i\")" % (int(pinid),int(repinboardid)))
                except:
                    print "Error inserting board:\n%s" % (pins[i])
             else:
                print "Board exists"
                cur.execute("SELECT boardid FROM Boards WHERE Boardname=\"%s\"" % (pins[i]))
                repinboardid=str(cur.fetchone()[0])
                cur.execute("INSERT INTO Pin_has_repinboards(Pins_Pinid,Boards_Boardid) VALUES (\"%i\",\"%i\")" % (int(pinid),int(repinboardid)))
            
        driver.close()
    return True

def getpins():
##    sqlpins="SELECT pinnum,pinid FROM Pins WHERE is_crawled='0' LIMIT 10"
    sqlpins="SELECT pinnum,pinid FROM Pins Where Pinid>210 LIMIT 10"
    cur.execute(sqlpins)
    pins=cur.fetchall()
    for item in pins:
        print item[1]
        print str(item[0])
        getinfo(item[0],item[1])
    conn.commit()
    return True



if __name__=="__main__":
    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='culturalcluster', passwd='W1nter0zturk', db='newpindb')
    cur = conn.cursor()

    getpins()

    cur.close()
    conn.close()
    






    
    
