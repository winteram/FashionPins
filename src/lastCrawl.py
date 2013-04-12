import pylast
import csv
import pymysql
import time
import re

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
    artistlist= csv.reader(open("../data/TopArtists.csv", "rb"))
    inartists=[]
    for data in artistlist:
        inartists.append(data[0])    
    #    print inartists
    cur.execute("TRUNCATE Tracks")
    cur.execute("TRUNCATE User")
    cur.execute("TRUNCATE Tags")
    cur.execute("TRUNCATE user_listens_tracks")
    cur.execute("TRUNCATE user_bans_tracks")
    cur.execute("TRUNCATE user_loves_tracks")
    cur.execute("TRUNCATE user_shouts_tracks")
    cur.execute("TRUNCATE tracks_has_tags")
    cur.execute("TRUNCATE user_has_friends")
    cur.execute("TRUNCATE user_recent_tracks")
    conn.commit()
    return inartists

def cleanName(name):
    name=name.encode('utf-8')
    if len(name) > 255:
        name = name[:255]
    name = re.sub("^'","",name)
    name = re.sub("'$","",name)
    name = re.sub('"','\"',name)
    return name

# get initial artists top 2 songs and the fans
def getinitial(inartists, cur):
    for y in range(0,len(inartists)):
    #for y in range(0,1):
        artist = network.get_artist(inartists[y])
        top_tracks=artist.get_top_tracks()
        # Tracks table
        trackar=[]
        for i in range(0,1):
            for top_track in top_tracks:
                # insert artist & trackname into tracks table
                trackar.append(top_track.item.get_name())
                tkey=str(artist)+'-'+trackar[i]
                if tkey not in tracklib:
                    tracklib[tkey]=1
    # print tracklib
    for item in tracklib:
        lartist=item.split('-')[0]
        ltrack=item.split('-')[1]
        ltrack = cleanName(ltrack)
        lartist = cleanName(lartist)
        #print (ltrack, lartist)
        cur.execute('INSERT INTO Tracks (is_crawled,track_name,artist_name) VALUES (0,"%s","%s")' % (ltrack,lartist))
        cur.execute('SELECT LAST_INSERT_ID()')
        trackid=int(cur.fetchone()[0])
        conn.commit()
        #print trackid
        try:
            track=network.get_track(lartist,ltrack)
        except:
            print "Track Error"
        else:
            cur.execute('SELECT is_crawled FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (ltrack,lartist))
            is_crawled=int(cur.fetchone()[0])
            #print is_crawled
            if is_crawled == 0:
            # Change the number of top fans here - if limit=None, returns 50
                topfans=track.get_top_fans()
                for topfan in topfans:
                    name=topfan.item.get_name()
                    cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                    cur.execute('SELECT LAST_INSERT_ID()')
                    userid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (%d,%d)' % (userid,trackid))
                    #print name + '-'+lartist +'-'+ ltrack
                    #print artistid
                cur.execute('UPDATE Tracks SET is_crawled=1 WHERE track_name="%s" AND artist_name="%s"' % (ltrack,lartist))
                conn.commit()
##    cur.execute('SELECT * FROM User')
##    user=cur.fetchall()
##    print user
##    cur.execute('SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute('SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens                                                                                                            
    return True

#get top tracks of fans - returns top 50 tracks
def toptracks():
    sqlfan='SELECT user_name, userid FROM User WHERE is_crawled=0'
    cur.execute(sqlfan)
    users=cur.fetchall()
    for item in users:
        userid=int(item[1])
        #print userid
        fan=network.get_user(str(item[0]))

        # Get top listened tracks
        try:
            print "getting top tracks for " +item[0]
            topfantracks=fan.get_top_tracks()
        except:
            print "Could not get top tracks for " + item[0]
        else:
            for topfantrack in topfantracks:
                track=topfantrack.item.get_name()
                if not track:
                    continue
                track_name=cleanName(track)
                artist=topfantrack.item.get_artist().get_name()
                artist_name=cleanName(artist)
                cur.execute('SELECT COUNT(1) FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (track_name,artist_name))
                if cur.fetchone()[0]==1:
                    cur.execute('SELECT trackid FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (track_name,artist_name))
                    trackid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (%d,%d)' % (userid,trackid))
                else:
                    try:
                        cur.execute('INSERT INTO Tracks(track_name,artist_name) VALUES ("%s","%s")' % (track_name,artist_name))
                    except:
                        print 'listens: name too long:\n%s\n%s' % (artist_name,track_name)
                    else:
                        track=cur.execute('SELECT LAST_INSERT_ID()')
                        trackid=int(cur.fetchone()[0])
                        # print trackid
                        cur.execute('INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (%d,%d)' % (userid,trackid))
                
        # Get loved tracks
        try:
            print "getting loved tracks for " + item[0]
            lovedtracks=fan.get_loved_tracks()
        except:
            print "Could not get loved tracks for " + item[0]
        else:
            for lovedtrack in lovedtracks:
                ltrack=lovedtrack.track.get_name()
                if not ltrack:
                    continue
                ltrack_name=cleanName(ltrack)
                ldate=lovedtrack.date
                ldate=ldate.split(",")[0]
                d=time.strptime(ldate, "%d %b %Y")
                ldate=time.strftime("%Y-%m-%d",d)
                lartist=lovedtrack.track.get_artist().get_name()
                lartist_name=cleanName(lartist)
                cur.execute('SELECT COUNT(1) FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (ltrack_name,lartist_name))
                if cur.fetchone()[0]==1:
                    cur.execute('SELECT trackid FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (ltrack_name,lartist_name))
                    ltrackid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_loves_tracks(user_userid,tracks_trackid,ldate) VALUES (%d,%d,"%s")' % (userid,ltrackid,ldate))
                else:
                    try:
                        cur.execute('INSERT INTO Tracks(track_name,artist_name) VALUES ("%s","%s")' % (ltrack_name,lartist_name))
                    except:
                        print 'loves: artist too long? %s, %s' % (lartist_name,ltrack_name)
                    else:
                        cur.execute('SELECT LAST_INSERT_ID()')
                        ltrackid=int(cur.fetchone()[0])
                        # print trackid
                        cur.execute('INSERT INTO user_loves_tracks(user_userid,tracks_trackid,ldate) VALUES (%d,%d,"%s")' % (userid,ltrackid,ldate))
               
        # Get banned tracks
        try:
            print "getting banned tracks for " + item[0]
            bannedtracks=fan.get_banned_tracks()
        except:
            print "Could not get banned tracks for " + item[0]
        else:
            for bannedtrack in bannedtracks:
                btrack=bannedtrack.track.get_name()
                if not btrack:
                    continue
                bdate=bannedtrack.date
                bdate=bdate.split(",")[0]
                d=time.strptime(bdate, "%d %b %Y")
                bdate=time.strftime("%Y-%m-%d",d)
                btrack_name=cleanName(btrack)
                bartist=bannedtrack.track.get_artist().get_name()
                bartist_name=cleanName(bartist)
                cur.execute('SELECT COUNT(1) FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (btrack_name,bartist_name))
                if cur.fetchone()[0]==1:
                    cur.execute('SELECT trackid FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (btrack_name,bartist_name))
                    btrackid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_bans_tracks(user_userid,tracks_trackid,bdate) VALUES (%d,%d,"%s")' % (userid,btrackid,bdate))
                else:
                    try:
                        cur.execute('INSERT INTO Tracks(track_name,artist_name) VALUES ("%s","%s")' % (btrack_name,bartist_name))
                    except:
                        print 'bans: artist too long? %s, %s' % (bartist_name,btrack_name)
                    else:
                        btrack=cur.execute('SELECT LAST_INSERT_ID()')
                        btrackid=int(cur.fetchone()[0])
                        # print trackid
                        cur.execute('INSERT INTO user_bans_tracks(user_userid,tracks_trackid,bdate) VALUES (%d,%d,"%s")' % (userid,btrackid,bdate))
        if bannedtracks:
            oldestbdate=bannedtracks[len(bannedtracks)-1].timestamp
            #print oldestbdate
        else:
            # if no banned tracks, set oldestbdate as Oct1,2012 for getting recent tracks 
            oldestbdate=1349049600
        
            
        # get friends
        try:
            print "getting friends for " +item[0]
            friends=fan.get_friends()
        except:
            print "Could not get friends for " + item[0]
        else:
            for friend in friends:
                friendname=friend.get_name()
                friendname=cleanName(friendname)
                #print friendname
                cur.execute('SELECT COUNT(1) FROM User WHERE user_name="%s"' , friendname)
                if cur.fetchone()[0] ==1:
                    cur.execute('SELECT userid FROM User Where user_name="%s"' , friendname)
                    friendid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_has_friends(User_userid,User_userid1) VALUES (%d,%d)' % (userid,friendid))
                else:
                    #print 'go ahead add'
                    cur.execute('INSERT INTO User SET user_name="%s"' % (friendname))
                    cur.execute('SELECT LAST_INSERT_ID()')
                    friendid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_has_friends(User_userid,User_userid1) VALUES (%d,%d)' % (userid,friendid))
        
        #Get recent tracks
        try:
            print "getting recent tracks for " + item[0]
            recents=fan.get_recent_tracks(from_d=oldestbdate)
            #print recents
        except:
            print "Could not get recent tracks for " + item[0]
        else:
            for recent in recents:
                rtrack=recent.track.get_name()
                if not rtrack:
                    continue
                rtrack_name=cleanName(rtrack)
                rartist=recent.track.get_artist().get_name()
                rartist_name=cleanName(rartist)
                rdate=recent.playback_date
                rdate=rdate.split(",")[0]
                d=time.strptime(rdate, "%d %b %Y")
                rdate=time.strftime("%Y-%m-%d",d)
                cur.execute('SELECT COUNT(1) FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (rtrack_name,rartist_name))
                if cur.fetchone()[0]==1:
                    cur.execute('SELECT trackid FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (rtrack_name,rartist_name))
                    rtrackid=int(cur.fetchone()[0])
                    cur.execute('INSERT INTO user_recent_tracks(User_userid,Tracks_trackid,date) VALUES (%d,%d,"%s")' % (userid,rtrackid,rdate))
                else:
                    try:
                        cur.execute('INSERT INTO Tracks(track_name,artist_name) VALUES ("%s","%s")' % (rtrack_name,rartist_name))
                    except:
                        print 'recents: artist too long? %s, %s' % (rartist_name,rtrack_name)
                    else:
                        cur.execute('SELECT LAST_INSERT_ID()')
                        rtrackid=int(cur.fetchone()[0])
                        # print trackid
                        cur.execute('INSERT INTO user_recent_tracks(User_userid,Tracks_trackid,date) VALUES (%d,%d,"%s")' % (userid,rtrackid,rdate))


        cur.execute('UPDATE User SET is_crawled=1 WHERE user_name="%s"' , item[0])             
        conn.commit()

        

##    cur.execute('SELECT * FROM User")
##    user=cur.fetchall()
##    print user
##    cur.execute('SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute('SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens
##    cur.execute('SELECT * FROM user_listens_tracks")
##    bans=cur.fetchall()
##    print bans
##    cur.execute('SELECT * FROM user_loves_tracks")
##    loves=cur.fetchall()
##    print loves 
    return True
        
### get topfans of tracks
def topfans():
    sqltracks='SELECT track_name, artist_name FROM Tracks WHERE is_crawled=0'
    cur.execute(sqltracks)
    tracks=cur.fetchall()
    #print tracks
    for item in tracks:
        track_name=cleanName(item[0])
        artist_name=cleanName(item[1])
        #print track_name + '-' + artist_name
        cur.execute('SELECT trackid FROM Tracks WHERE track_name="%s" AND artist_name="%s"' % (track_name,artist_name))
        trackid=int(cur.fetchone()[0])
        #print trackid+ '-' + 'trackname: ' + track_name + ' artistname: ' + artist_name
        try:
            track=network.get_track(artist_name,track_name)
        except:
            print "track error"
        else:
            # Track TopFans - Change the number of top fans here - if limit=None, returns 50
            try:
            	#topfans=track.get_top_fans(limit=1)
                topfans=track.get_top_fans(limit=None)
            except:
                print "fans error"
            else:
                for topfan in topfans:
                    name=topfan.item.get_name()
                    name=cleanName(name)
                    cur.execute('SELECT COUNT(1) FROM User WHERE user_name="%s"' , name)
                    #print name
                    if cur.fetchone()[0]!=1:
                        #print name + ' -'+' User already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                        cur.execute('SELECT LAST_INSERT_ID()')
                        userid=int(cur.fetchone()[0])
                        cur.execute('INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (%d,%d)' % (userid,trackid))
                        #print name + '-'+artist_name +'-'+ track_name
                        #print artistid
            #Track Shouts
            try:
            	shouts=track.get_shouts()
            except:
                print "shout error"
            else:
                for shout in shouts:
                    name1=shout[1].get_name()
                    name=cleanName(name1)
                    cur.execute('SELECT COUNT(1) FROM User WHERE user_name="%s"' , name)
                    #print name
                    if cur.fetchone()[0]!=1:
                        #print name + ' -'+' User already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                        cur.execute('SELECT LAST_INSERT_ID()')
                        suserid=int(cur.fetchone()[0])
                        cur.execute('INSERT INTO user_shouts_tracks(user_userid,tracks_trackid) VALUES (%d,%d)' % (suserid,trackid))
                       
            # Track Tags
            try:
            	tags=track.get_top_tags()
            except:
                print "Tag error"
            else:
                for tag in tags:
                    tagtext1=tag.item.get_name()
                    tagtext=cleanName(tagtext1)
                    #print tagtext
                    cur.execute('SELECT COUNT(1) FROM Tags WHERE tag_text="%s"' , tagtext)
                    #print tagtext
                    if cur.fetchone()[0]!=1:
                        #print tagtext + ' -'+' Tag already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO Tags SET tag_text="%s"' % (tagtext))
                        cur.execute('SELECT LAST_INSERT_ID()')
                        tagid=int(cur.fetchone()[0])
                        cur.execute('INSERT INTO tracks_has_tags(tags_tagid,tracks_trackid) VALUES (%d,%d)' % (tagid,trackid))
                
                
            cur.execute('UPDATE Tracks SET is_crawled=1 WHERE track_name="%s" AND artist_name="%s"' % (track_name,artist_name))
            conn.commit()
##    cur.execute('SELECT * FROM User")
##    user=cur.fetchall()
##    print user
##    cur.execute('SELECT * FROM Tracks")
##    tracks=cur.fetchall()
##    print tracks
##    cur.execute('SELECT * FROM user_listens_tracks")
##    listens=cur.fetchall()
##    print listens
    return True




if __name__=="__main__":
    conn = pymysql.connect(host='wmason.mgnt.stevens-tech.edu', port=3306, user='culturalcluster', passwd='W1nter0zturk', db='ccdb')
    cur = conn.cursor()
    restart = True
    # TODO: put in command-line argument for restart or continue
    if restart:
        print "Getting initial artists"
        inartists=getartist(cur)
        print "Getting initial tracks and users"
        tracklib=getinitial(inartists, cur)
    #tracks=toptracks()
    #fans=topfans()

    for z in range(0,1):     
        print "Getting top tracks"
        tracks=toptracks()
        print "Getting top fans"
        fans=topfans()
    cur.close()
    conn.close()

