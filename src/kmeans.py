import numpy as np
from sklearn import cluster
import collections
from random import randint
import math
import pymysql
from pylab import plot,show

def randomboard(board1):
#    # Get # of boards crawled
#    cur.execute("SELECT COUNT(*) FROM Boards where is_crawled=1")
#    allboards=cur.fetchone()[0]
#    #print "Boards number: " + str(allboards)
#
#    # Get first random boardid
#    board1=randint(1,allboards)
#    #print "Random Board1: " + str(board1)

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
        #print str(item[0])
        cur.execute("SELECT Sources_sourceid FROM Pin_has_sources WHERE Pins_pinid=\"%s\"" % str(item[0]))
        source=cur.fetchone()
        if source != None:
            board1sources.append(int(source[0]))
    #print "Board1 sources: " + str(len(board1sources))
    

    return board1,board1sources

def getboards():
    correlations = np.genfromtxt('/Users/pinarozturk/Documents/LastFm/cosdicteach150.csv', delimiter=',')
    headers = correlations[0,:] [1:]
    #print headers
    boards=[]
    for item in headers:
        boards.append(int(item))
    #print boards
    return boards
if __name__=="__main__":

    conn = pymysql.connect(host='localhost', unix_socket='/tmp/mysql.sock', user='pinarozturk', passwd='', db='pindb')
    cur = conn.cursor()
    selectedboards=getboards()
    
    
    sourcedict=collections.OrderedDict()
    board1a=[]
    board2a=[]
    cossima=[]
    board1so=[]
    #selectedboards=[1,2,10,3,4,5,9,6,7,8]
    for a in range(0,len(selectedboards)):
        #print a
        #for i in range(0,8):
            #print i
        board1,board1s=randomboard(selectedboards[a])
        #if board1s==[]:
        #    continue
        board1so.append(board1s)
        board1a.append(board1)
        key=board1
        if key not in sourcedict:
            sourcedict[key]=board1s
            
    #print sourcedict
    print "Boards: " + str(sourcedict.keys())
    #print len(board1a)
    #print len(sourcedict.items())
    board1so = [val for subl in board1so for val in subl]
    featuredict={}
    for i in range(0,len(board1a)):
        for a in range(0,len(board1so)):
            #print board1so[a]
            #print board1a[i]
            if board1so[a] in sourcedict[board1a[i]]:
                #print "yes"
                key=board1a[i]
                if key not in featuredict:
                    featuredict.setdefault(key,[]).append(1) 
                else:
                    featuredict.setdefault(key,[]).append(1) 
            else:
                #print "no"
                key=board1a[i]
                #print "Key:" + str(key)
                if key not in featuredict:
                    featuredict.setdefault(key,[]).append(1) 
                else:
                    featuredict.setdefault(key,[]).append(0) 

    #print featuredict
    #print len(featuredict)
    featurearray=[]
    for i in range(0,len(board1a)):
        featurearray.append(featuredict[board1a[i]])
    #print featurearray
    
    print " "
    k=5
    #print selectedboards
    centroids, labels, inertia = cluster.k_means(featurearray, k)
    print "Centroids: " + str(centroids)
    print " "
    print "Clusters: " + str(labels)
    print " "
    #print labels.max()
    #print len(np.unique(labels))
   
    clustername=[]
    for i in range(0,len(np.unique(labels))):
        npindex=np.where(labels==np.unique(labels)[i])
        #print npindex[0]
        for a in range(len(npindex[0])):
            clustername.append(selectedboards[npindex[0][a]])
            clustername.sort(reverse=True)
        print 'Cluster ' + str(i+1)+ ': '+ str(clustername)
        clustername=[]
    print inertia
    

    cur.close()
    conn.close()