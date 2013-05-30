
import math
import pymysql
import random
from random import randint
import csv
import collections



def randomboard():
    # Get # of boards crawled
    cur.execute("SELECT COUNT(*) FROM Boards where is_crawled=1")
    allboards=cur.fetchone()[0]
    #print "Boards number: " + str(allboards)

    # Get first random boardid
    board1=randint(1,allboards)
    #print "Random Board1: " + str(board1)

    # Get first board pins
    cur.execute("SELECT COUNT(*) From Board_has_pins where Boards_boardid=\"%i\"" % (board1))
    board1pinnum=cur.fetchone()[0]
    #print "Board1 pins: " + str(board1pinnum)

    #Get first board pin sources
    cur.execute("SELECT Pins_pinid FROM Board_has_pins where Boards_boardid=\"%i\"" % (board1))
    board1pins=cur.fetchall()
    #print len(board1pins)
    board1sources=[]
    for item in board1pins:
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        board1sources.append(cur.fetchall())
    #print "Board1 sources: " + str(len(board1sources))



    # Get second random board
    board2=randint(1,allboards)
    #print "Random Board2: " + str(board2)

    # Get second board pins
    cur.execute("SELECT COUNT(*) From Board_has_pins where Boards_boardid=\"%i\"" % (board2))
    board2pinnum=cur.fetchone()[0]
    #print "Board2 pins: " + str(board2pinnum)

    # Get second board pin sources
    cur.execute("SELECT Pins_pinid FROM Board_has_pins where Boards_boardid=\"%i\"" % (board2))
    board2pins=cur.fetchall()
    board2sources=[]
    for item in board2pins:
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        board2sources.append(cur.fetchall())
    #print "Board2 sources: " + str(len(board2sources))

   
    # Find intersection of first board sources & second board sources
    a,b=set(board1sources), set(board2sources)
    intersect= len(a.intersection(b))
    #print intersect
    #print a & b
    
    
    return intersect



if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()
    intersect=[]

    # Write to csv file to use in visualization
    f = open("random.csv","wb")
    writer = csv.writer(f)
    row = [ "intersect"]
    writer.writerow(row)
    for i in range(0,1000):
        #print i
        num=randomboard()
        writer.writerow([num])
        intersect.append(num)
    #print intersect
        
    y=collections.Counter(intersect)
    print y.items()
    f.close()

    
    cur.close()
    conn.close()
