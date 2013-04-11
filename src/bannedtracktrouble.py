import pylast
import csv
import pymysql
import time

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)

tracklib={}
trackar=[]
fans=[]
tracks=[]
artists=[]
artistlist=[]
tracklist=[]
userlist=[]
bannedlist={}

fanlib={}


#get top tracks of fans - returns top 50 tracks
def toptracks():
    sqlfan="SELECT user_name FROM User WHERE is_crawled='1' LIMIT 26,4"
    cur.execute(sqlfan)
    users=cur.fetchall()
    print "Printing all users gotten from database: "+ str(users)
    for item in users:
        print "Printing each user: " + str(item[0])
        cur.execute("SELECT userid FROM User WHERE user_name=\"%s\"" % item)
        userid=str(cur.fetchone()[0])
        #print userid
        fan=network.get_user(str(item[0]))

        # Get banned tracks
        try:
            print "getting banned tracks for " + item[0]
            bannedtracks=fan.get_banned_tracks()
            print bannedtracks
        except:
            print "Could not get banned tracks for " + item[0]
        else:
            for bannedtrack in bannedtracks:
                btrack=bannedtrack.track.get_name()
                print "--"
                if not btrack:
                    continue
                bdate=bannedtrack.date
                bdate=bdate.split(",")[0]
                d=time.strptime(bdate, "%d %b %Y")
                bdate=time.strftime("%Y-%m-%d",d)
                btrack_name=btrack.encode('utf-8')
                
                if len(btrack_name) > 255:
                    btrack_name = btrack_name[:255]
                bartist=bannedtrack.track.get_artist().get_name()
                bartist_name=bartist.encode('utf-8')
                if len(bartist_name) > 255:
                    bartist_name = bartist_name[:255]
                print "Banned track name is: " + str(btrack_name) + ' - '+str(bartist_name)
                key=bartist_name+'-'+btrack_name+'-'+str(item[0])
                #print key
##                if key not in bannedlist:
##                    bannedlist[key]=1
##                    print "writing to csv"
##                    writer.writerow([item[0],btrack_name,bartist_name,bdate])
##                    print "Banned list length: " + str(len(bannedlist))
                cur.execute("SELECT COUNT(1) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (btrack_name,bartist_name))
                #trackid2=cur.fetchone()[0]
                #print trackid2
                if (cur.fetchone()[0])==1:
                    print "Existing Track: " + " - "+ btrack_name +" - "+ bartist_name
                    cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (btrack_name,bartist_name))
                    btrackid=str(cur.fetchone()[0])
                    print btrackid
                    cur.execute("SELECT COUNT(1) FROM user_bans_tracks WHERE user_userid=\"%s\" AND tracks_trackid=\"%s\"" % (userid,btrackid))
                    if cur.fetchone()[0]==0:
                        print "Bannedtrack doesn't exist, will insert!!!!!!!!!!"
                        cur.execute("INSERT INTO user_bans_tracks(user_userid,tracks_trackid,bdate) VALUES (\"%s\",\"%s\",\"%s\")" % (userid,btrackid,bdate))
                    else:
                        print "Bannedtrack already exists"
                else:
                    try:
                        print "Inserting new track into tracks"
                        cur.execute("INSERT INTO Tracks(track_name,artist_name) VALUES (\"%s\",\"%s\")" % (btrack_name,bartist_name))
                        btrack=cur.execute("SELECT LAST_INSERT_ID()")
                        btrackid=str(cur.fetchone()[0])
                    except:
                        print "bans: artist too long? %s, %s" % (bartist_name,btrack_name)
                    else:
                        cur.execute("SELECT COUNT(1) FROM user_bans_tracks WHERE user_userid=\"%s\" AND tracks_trackid=\"%s\"" % (userid,btrackid))
                        if cur.fetchone()[0]!=1:
                            print "Bannedtrack doesn't exist, will insert!!!!!!!!!"
                            print "Inserting into bans tracks - Trackid: " 
                            cur.execute("INSERT INTO user_bans_tracks(user_userid,tracks_trackid,bdate) VALUES (\"%s\",\"%s\",\"%s\")" % (userid,btrackid,bdate))
                
        conn.commit()

        cur.execute("SELECT * FROM user_bans_tracks WHERE user_userid=\"%s\"" % (userid))
        bans=cur.fetchall()
        print "Inserted banned tracks:" +str(bans) 
        print "*************"
    return True

            
        



if __name__=="__main__":
    conn = pymysql.connect(host='wmason.mgnt.stevens-tech.edu', port=3306, user='culturalcluster', passwd='W1nter0zturk', db='ccdb')
    cur = conn.cursor()

    

     # Exists (trackid=100696) - if "%" is changed to "," it returns trackid of 22652
    trackn2="Bad Side of 25"
    artistn2="Patrick Stump"
    print trackn2 + '-' + artistn2
    cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn2,artistn2))
    print str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn2,artistn2))
    print "Count:" +str(cur.fetchone()[0]) 

    # Exists (trackid=22652) - If "%" is changed to "," it returns None, gives error
    trackn3="'Bad Side of 25'"
    artistn3="'Patrick Stump'"
    print trackn3 +'-'+artistn3
    cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn3,artistn3))
    print str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn3,artistn3))
    print "Count: " + str(cur.fetchone()[0])


    # Doesn't exist - If "%", it returns None, gives error (how it should be)
    trackn="People"
    artistn="Gorillaz"
    print trackn + '-' + artistn
    cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (trackn,artistn))
    print str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (trackn,artistn))
    print "Count:" +str(cur.fetchone()[0]) 

    # Exists (trackid=33560)
    trackn1="'People'"
    artistn1="'Gorillaz'"
    print trackn1 +'-'+artistn1
    cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn1,artistn1))
    print str(cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (trackn1,artistn1))
    print "Count: " + str(cur.fetchone()[0])
    
##    try:
##        f = open("bannedtracks.csv","r+")
##        print "f open"
##    except IOError:
##        print "Error opening bannedtracks.csv"
##        sys.exit(0)
##    else:
##        writer=csv.writer(f)
##        row = [ "user", "banned track","banned track artist","ban date"]
##        print "row written"
##        writer.writerow(row)

    
        
    
    print "Getting banned tracks"
    tracks=toptracks()



##    f.close()
    cur.close()
    conn.close()

