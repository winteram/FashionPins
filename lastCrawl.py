import pylast
import csv
import pymysql

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

fanlib={}


# get initial top 100 artists and their top 2 tracks
def getartist(cur):
    artistlist= csv.reader(open("TopArtists.csv", "rb"))
    inartists=[]
    for data in artistlist:
        inartists.append(data[0])    
#    print inartists
    cur.execute("TRUNCATE Tracks;")
    cur.execute("TRUNCATE User;")
    cur.execute("TRUNCATE user_listens_tracks;")
    conn.commit()
    return inartists

# get initial artists top 2 songs and the fans
def getinitial(inartists, cur):
##for y in range(0,len(inartists)):
    for y in range(0,1):
        artist = network.get_artist(inartists[y])
        top_tracks=artist.get_top_tracks()
        trackar=[]
        for i in range(0,1):
            for top_track in top_tracks:
                trackar.append(top_track.item.get_name())
                tkey=str(artist)+'-'+trackar[i]
                if tkey not in tracklib:
                    tracklib[tkey]=1
#    print tracklib
    for item in tracklib:
        lartist=item.split('-')[0]
        ltrack=item.split('-')[1]
        print (ltrack, lartist)
        sql="INSERT INTO Tracks (is_crawled,track_name,artist_name) VALUES (0,'%s','%s')" % (ltrack,lartist)
        cur.execute(sql)
        cur.execute("SELECT LAST_INSERT_ID()")
        trackid=str(cur.fetchone()[0])
        conn.commit()
        #print trackid
        try:
            track=network.get_track(lartist,ltrack)
        except:
            print "Track Error"
        else:
            cur.execute("SELECT is_crawled FROM Tracks WHERE track_name='%s' AND artist_name='%s'" % (ltrack,lartist))
            is_crawled=str(cur.fetchone()[0])
            print is_crawled
            if is_crawled == '0':
            # Change the number of top fans here - if limit=None, returns 50
                topfans=track.get_top_fans(limit=1)
                for topfan in topfans:
                    name=topfan.item.get_name()
                    cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                    cur.execute("SELECT LAST_INSERT_ID()")
                    userid=str(cur.fetchone()[0])
                    cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES ('%s','%s')" % (userid,trackid))
                    print name + '-'+lartist +'-'+ ltrack
                    #print artistid
                cur.execute("UPDATE Tracks SET is_crawled='1' WHERE track_name='%s' AND artist_name='%s'" % (ltrack,lartist))
                conn.commit()
##    cur.execute("SELECT * FROM User")
##    user=cur.fetchall()
##    print user
##    cur.execute("SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute("SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens                                                                                                            
    return True

#get top tracks of fans - returns top 50 tracks
def toptracks():
    sqlfan="SELECT user_name FROM User WHERE is_crawled='0'"
    cur.execute(sqlfan)
    users=cur.fetchall()
    for item in users:
        cur.execute("SELECT userid FROM User WHERE user_name='%s'" % item)
        userid=str(cur.fetchone()[0])
        print userid
        fan=network.get_user(str(item[0]))
        topfantracks=fan.get_top_tracks()
        for topfantrack in topfantracks:
            track=topfantrack.item.get_name()
            track_name=track.encode('utf-8')
            if len(track_name) > 255:
                track_name = track_name[:255]
            artist=topfantrack.item.get_artist().get_name()
            artist_name=artist.encode('utf-8')
            cur.execute("SELECT COUNT(1) FROM Tracks WHERE track_name=%s AND artist_name=%s" , (track_name,artist_name))
            if cur.fetchone()[0]==1:
                print track_name + ' - ' +artist_name + ' -'+' Track already exists'
            else:
                cur.execute("INSERT INTO Tracks(track_name,artist_name) VALUES (%s,%s)" , (track_name,artist_name))
                track=cur.execute("SELECT LAST_INSERT_ID()")
                trackid=str(cur.fetchone()[0])
                #print trackid
                cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES ('%s','%s')" % (userid,trackid))
                cur.execute("UPDATE User SET is_crawled='1' WHERE user_name='%s'" % item[0])             
##    cur.execute("SELECT * FROM User")
##    user=cur.fetchall()
##    print user
##    cur.execute("SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute("SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens 
    return True
        
### get topfans of tracks
def topfans():
    sqltracks="SELECT track_name, artist_name FROM Tracks WHERE is_crawled='0'"
    cur.execute(sqltracks)
    tracks=cur.fetchall()
    #print tracks
    for item in tracks:
        track_name=item[0]
        if len(track_name) > 255:
            track_name = track_name[:255]
        artist_name=item[1]
        cur.execute("SELECT trackid FROM Tracks WHERE track_name=%s AND artist_name=%s" , (track_name,artist_name))
        trackid=str(cur.fetchone()[0])
        #print trackid+ '-' + 'trackname: ' + track_name + ' artistname: ' + artist_name
        try:
            track=network.get_track(artist_name,track_name)
        except:
            print "track error"
        else:
            # Change the number of top fans here - if limit=None, returns 50
            try:
            	topfans=track.get_top_fans(limit=1)
            except:
                print "fans error"
            else:
                for topfan in topfans:
                    name=topfan.item.get_name()
                    cur.execute("SELECT COUNT(1) FROM User WHERE user_name=%s" , name)
                    #print name
                    if cur.fetchone()[0]==1:
                        print name + ' -'+' User already exists--------'
                    else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                        cur.execute("SELECT LAST_INSERT_ID()")
                        userid=str(cur.fetchone()[0])
                        cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES ('%s','%s')" % (userid,trackid))
                        #print name + '-'+artist_name +'-'+ track_name
                        #print artistid
                        cur.execute("UPDATE Tracks SET is_crawled='1' WHERE track_name=%s AND artist_name=%s" , (track_name,artist_name))
##    cur.execute("SELECT * FROM User")
##    user=cur.fetchall()
##    print user
##    cur.execute("SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute("SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens
    return True




if __name__=="__main__":
    conn = pymysql.connect(host='wmason.mgnt.stevens-tech.edu', port=3306, user='culturalcluster', passwd='W1nter0zturk', db='ccdb')
    cur = conn.cursor()

    inartists=getartist(cur)
    tracklib=getinitial(inartists, cur)
    #tracks=toptracks()
    #fans=topfans()

    #for z in range(0,2):     
    #    tracks,fanlib=toptracks(fans)
    #   fans=topfans(tracks)
    cur.close()
    conn.close()

