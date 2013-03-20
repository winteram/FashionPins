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
    cur.execute("TRUNCATE Friends")
    cur.execute("TRUNCATE user_listens_tracks")
    cur.execute("TRUNCATE user_bans_tracks")
    cur.execute("TRUNCATE user_loves_tracks")
    cur.execute("TRUNCATE user_shouts_tracks")
    cur.execute("TRUNCATE tracks_has_tags")
    cur.execute("TRUNCATE user_has_friends")
    conn.commit()
    return inartists

# get initial artists top 2 songs and the fans
def getinitial(inartists, cur):
    for y in range(0,len(inartists)):
    # for y in range(0,1):
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
        if ltrack.startswith("'") and ltrack.endswith("'"):
            ltrack = ltrack[1:-1]
        if lartist.startswith("'") and lartist.endswith("'"):
            lartist = lartist[1:-1]
        #print (ltrack, lartist)
        sql="INSERT INTO Tracks (is_crawled,track_name,artist_name) VALUES (0,\"%s\",\"%s\")" % (ltrack,lartist)
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
            cur.execute("SELECT is_crawled FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (ltrack,lartist))
            is_crawled=str(cur.fetchone()[0])
            #print is_crawled
            if is_crawled == '0':
            # Change the number of top fans here - if limit=None, returns 50
                topfans=track.get_top_fans()
                for topfan in topfans:
                    name=topfan.item.get_name()
                    cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                    cur.execute("SELECT LAST_INSERT_ID()")
                    userid=str(cur.fetchone()[0])
                    cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (\"%s\",\"%s\")" % (userid,trackid))
                    #print name + '-'+lartist +'-'+ ltrack
                    #print artistid
                cur.execute("UPDATE Tracks SET is_crawled='1' WHERE track_name=\"%s\" AND artist_name=\"%s\"" % (ltrack,lartist))
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
        cur.execute("SELECT userid FROM User WHERE user_name=\"%s\"" % item)
        userid=str(cur.fetchone()[0])
        #print userid
        fan=network.get_user(str(item[0]))

        # Get top listened tracks
        try:
            topfantracks=fan.get_top_tracks()
        except:
            print "Could not get top tracks for " + item[0]
        else:
            for topfantrack in topfantracks:
                track=topfantrack.item.get_name()
                if not track:
                    continue
                track_name=track.encode('utf-8')
                if len(track_name) > 255:
                    track_name = track_name[:255]
                if track_name.startswith("'") and track_name.endswith("'"):
                    track_name = track_name[1:-1]
                artist=topfantrack.item.get_artist().get_name()
                artist_name=artist.encode('utf-8')
                if len(artist_name) > 255:
                    artist_name = artist_name[:255]
                if artist_name.startswith("'") and artist_name.endswith("'"):
                    artist_name = artist_name[1:-1]
                cur.execute("SELECT COUNT(1) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (track_name,artist_name))
                if cur.fetchone()[0]!=1:
                #print track_name + ' - ' +artist_name + ' -'+' Track already exists'
            #else:
                    try:
                        cur.execute("INSERT INTO Tracks(track_name,artist_name) VALUES (\"%s\",\"%s\")" , (track_name,artist_name))
                    except:
                        print "name too long:\n%s\n%s" % (artist_name,track_name)
                    else:
                        track=cur.execute("SELECT LAST_INSERT_ID()")
                        trackid=str(cur.fetchone()[0])
                        # print trackid
                        cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (\"%s\",\"%s\")" % (userid,trackid))
                
        # Get loved tracks
        try:
            lovedtracks=fan.get_loved_tracks()
        except:
            print "Could not get loved tracks for " + item[0]
        else:
            for lovedtrack in lovedtracks:
                ltrack=lovedtrack.track.get_name()
                if not ltrack:
                    continue
                ldate=lovedtrack.date
                ldate=ldate.split(",")[0]
                d=time.strptime(ldate, "%d %b %Y")
                ldate=time.strftime("%Y-%m-%d",d)
                ltrack_name=ltrack.encode('utf-8')
                if len(ltrack_name) > 255:
                    ltrack_name = ltrack_name[:255]
                if ltrack.startswith("'") and ltrack.endswith("'"):
                    ltrack = ltrack[1:-1]
                lartist=lovedtrack.track.get_artist().get_name()
                lartist_name=lartist.encode('utf-8')
                if len(lartist_name) > 255:
                    lartist_name = lartist_name[:255]
                if lartist.startswith("'") and lartist.endswith("'"):
                    lartist = lartist[1:-1]
                cur.execute("SELECT COUNT(1) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (ltrack_name,lartist_name))
                if cur.fetchone()[0]!=1:
                #print ltrack_name + ' - ' +lartist_name + ' -'+' Track already exists'
            #else:
                    try:
                        cur.execute("INSERT INTO Tracks(track_name,artist_name) VALUES (\"%s\",\"%s\")" , (ltrack_name,lartist_name))
                    except:
                        print "artist too long? %s, %s" % (lartist_name,ltrack_name)
                    else:
                        btrack=cur.execute("SELECT LAST_INSERT_ID()")
                        ltrackid=str(cur.fetchone()[0])
                        # print trackid
                        cur.execute("INSERT INTO user_loves_tracks(user_userid,tracks_trackid,ldate) VALUES (\"%s\",\"%s\",\"%s\")" % (userid,ltrackid,ldate))
                
        # Get banned tracks
        try:
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
                btrack_name=btrack.encode('utf-8')
                if len(btrack_name) > 255:
                    btrack_name = btrack_name[:255]
                bartist=bannedtrack.track.get_artist().get_name()
                bartist_name=bartist.encode('utf-8')
                if len(bartist_name) > 255:
                    bartist_name = bartist_name[:255]
                cur.execute("SELECT COUNT(1) FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (btrack_name,bartist_name))
                if cur.fetchone()[0]!=1:
                #print btrack_name + ' - ' +bartist_name + ' -'+' Track already exists'
            #else:
                    try:
                        cur.execute("INSERT INTO Tracks(track_name,artist_name) VALUES (\"%s\",\"%s\")" , (btrack_name,bartist_name))
                    except:
                        print "artist too long? %s, %s" % (bartist_name,btrack_name)
                    else:
                        btrack=cur.execute("SELECT LAST_INSERT_ID()")
                        btrackid=str(cur.fetchone()[0])
                        # print trackid
                        cur.execute("INSERT INTO user_bans_tracks(user_userid,tracks_trackid,bdate) VALUES (\"%s\",\"%s\",\"%s\")" % (userid,btrackid,bdate))

        # get friends
        try:
            friends=fan.get_friends()
        except:
            print "Could not get friends for " + item[0]
        else:
            for friend in friends:
                friendname=friend.get_name()
                friendname=friendname.encode('utf-8')
                if len(friendname) > 255:
                    friendname = friendname[:255]
                #print friendname
                cur.execute("SELECT COUNT(1) FROM Friends WHERE friend_name=\"%s\"" , friendname)
                if cur.fetchone()[0] ==1:
                    cur.execute("SELECT friendid FROM Friend Where friend_name=\"%s\"" , friendname)
                    friendid=str(cur.fetchone()[0])
                    cur.execute("INSERT INTO user_has_friends(User_userid,Friends_friendid) VALUES (\"%s\",\"%s\")" % (userid,friendid))
                else:
                    #print 'go ahead add'
                    cur.execute('INSERT INTO Friends SET friend_name="%s"' % (friendname))
                    cur.execute("SELECT LAST_INSERT_ID()")
                    friendid=str(cur.fetchone()[0])
                    cur.execute("INSERT INTO user_has_friends(User_userid,Friends_friendid) VALUES (\"%s\",\"%s\")" % (userid,friendid))

                


        cur.execute("UPDATE User SET is_crawled='1' WHERE user_name=\"%s\"" % item[0])             
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
##    cur.execute("SELECT * FROM user_listens_tracks")
##    bans=cur.fetchall()
##    print bans
##    cur.execute("SELECT * FROM user_loves_tracks")
##    loves=cur.fetchall()
##    print loves 
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
        if track_name.startswith("'") and track_name.endswith("'"):
            track_name = track_name[1:-1]
        artist_name=item[1]
        if artist_name.startswith("'") and artist_name.endswith("'"):
            artist_name = artist_name[1:-1]
        #print track_name + '-' + artist_name
        cur.execute("SELECT trackid FROM Tracks WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (track_name,artist_name))
        trackid=str(cur.fetchone()[0])
        #print trackid+ '-' + 'trackname: ' + track_name + ' artistname: ' + artist_name
        try:
            track=network.get_track(artist_name,track_name)
        except:
            print "track error"
        else:
            # Track TopFans - Change the number of top fans here - if limit=None, returns 50
            try:
            	topfans=track.get_top_fans()
            except:
                print "fans error"
            else:
                for topfan in topfans:
                    name=topfan.item.get_name()
                    cur.execute("SELECT COUNT(1) FROM User WHERE user_name=\"%s\"" , name)
                    #print name
                    if cur.fetchone()[0]!=1:
                        #print name + ' -'+' User already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                        cur.execute("SELECT LAST_INSERT_ID()")
                        userid=str(cur.fetchone()[0])
                        cur.execute("INSERT INTO user_listens_tracks(user_userid,tracks_trackid) VALUES (\"%s\",\"%s\")" % (userid,trackid))
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
                    name=name1.encode('utf-8')
                    cur.execute("SELECT COUNT(1) FROM User WHERE user_name=\"%s\"" , name)
                    #print name
                    if cur.fetchone()[0]!=1:
                        #print name + ' -'+' User already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO User SET user_name="%s"' % (name))
                        cur.execute("SELECT LAST_INSERT_ID()")
                        suserid=str(cur.fetchone()[0])
                        cur.execute("INSERT INTO user_shouts_tracks(user_userid,tracks_trackid) VALUES (\"%s\",\"%s\")" % (suserid,trackid))
                       
            # Track Tags
            try:
            	tags=track.get_top_tags()
            except:
                print "Tag error"
            else:
                for tag in tags:
                    tagtext1=tag.item.get_name()
                    tagtext=tagtext1.encode('utf-8')
                    if len(tagtext) > 255:
                        tagtext = tagtext[:255]
                    #print tagtext
                    cur.execute("SELECT COUNT(1) FROM Tags WHERE tag_text=\"%s\"" , tagtext)
                    #print tagtext
                    if cur.fetchone()[0]!=1:
                        #print tagtext + ' -'+' Tag already exists'
                    #else:
                        #print 'go ahead add'
                        cur.execute('INSERT INTO Tags SET tag_text="%s"' % (tagtext))
                        cur.execute("SELECT LAST_INSERT_ID()")
                        tagid=str(cur.fetchone()[0])
                        cur.execute("INSERT INTO tracks_has_tags(tags_tagid,tracks_trackid) VALUES (\"%s\",\"%s\")" % (tagid,trackid))
                
                
            cur.execute("UPDATE Tracks SET is_crawled='1' WHERE track_name=\"%s\" AND artist_name=\"%s\"" , (track_name,artist_name))
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

    for z in range(0,3):     
        print "Getting top tracks"
        tracks=toptracks()
        print "Getting top fans"
        fans=topfans()
    cur.close()
    conn.close()

