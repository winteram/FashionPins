
import math
import pymysql
from random import randint
import csv
import collections
import pylast
from pandas import DataFrame

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)

uniontracks=[]
intersecttracks=[]



def randomuser():
    # Get # of boards crawled
    cur.execute("SELECT * FROM User_bans_tracks ORDER By User_userid DESC Limit 1")
    users=cur.fetchone()[0]
    #print "Users number: " + str(users)

    # Get first random user
    user1=randint(1,users)
    #print "Random User1: " + str(user1)

    # Get first user banned tracks
    cur.execute("SELECT COUNT(*) From User_bans_tracks where User_userid=\"%i\"" % (user1))
    user1bannednum=cur.fetchone()[0]
    #print "User1 banned track number: " + str(user1bannednum)

    
    cur.execute("SELECT Tracks_trackid FROM User_bans_tracks where User_userid=\"%i\"" % (user1))
    user1banned=[]
    user1banned.append(cur.fetchall())
    #print "User1 banned tracks: " +str(user1banned)

    # Get second random user
    user2=randint(1,users)
    #print "Random User2: " + str(user2)

    # Get first user banned tracks
    cur.execute("SELECT COUNT(*) From User_bans_tracks where User_userid=\"%i\"" % (user2))
    user2bannednum=cur.fetchone()[0]
    #print "User2 banned track number: " + str(user2bannednum)

    
    cur.execute("SELECT Tracks_trackid FROM User_bans_tracks where User_userid=\"%i\"" % (user2))
    user2banned=[]
    user2banned.append(cur.fetchall())
    #print "User2 banned tracks: " +str(user2banned)

    # Find intersection of first user banned tracks & second user banned tracks
    a,b=set(user1banned), set(user2banned)
    if user1bannednum==0 or user2bannednum==0:
        intersect=0
        #print "Intersect: " + str(intersect)
    else:
        intersect= len(a.intersection(b))
        #print "Intersect: " + str(intersect)
        
    intersecttracks.append(intersect)
    union=user1bannednum+user2bannednum-intersect
    uniontracks.append(union)
   
    return True



if __name__=="__main__":

    conn = pymysql.connect(host='wmason.mgnt.stevens-tech.edu', port=3306, user='culturalcluster', passwd='W1nter0zturk', db='ccdb')
    cur = conn.cursor()

    for i in range(0,250):
        randomuser()


    btrackdict={}
    btrack={}

    #print "Union: " + str(uniontracks)
    #print "Intersect: " + str(intersecttracks)
    
    for a in range(len(uniontracks)):
        key=str(uniontracks[a])+'-'+str(intersecttracks[a])
        #print key
        if key not in btrackdict:
            btrackdict[key]=1
        else:
            btrackdict[key]+=1

    #print btrackdict
    

    c=collections.Counter(uniontracks)
    d=collections.Counter(intersecttracks)

    for i in range(0,len(c)):
        btrack[list(c)[i]]={}
        for y in range(len(d)):
            key2=str(list(c)[i])+'-'+str(list(d)[y])
            #print key2
            if key2 in btrackdict:
                btrack[list(c)[i]][list(d)[y]]=btrackdict[key2]
            else:
                btrack[list(c)[i]][list(d)[y]]=0
            
    
    #print "{Union: {Intersect: Freq} " +str(btrack)    

    df = DataFrame(btrack)
    df.to_csv('../data/btrack.csv')
    
    
    cur.close()
    conn.close()
