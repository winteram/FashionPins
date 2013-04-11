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


# get initial top 100 artists and their top 2 tracks
def getartist():
    artistlist= csv.reader(open("TopArtists.csv", "rb"))
    inartists=[]
    for data in artistlist:
        inartists.append(data[0])    
    #    print inartists
    return inartists

# get initial artists top 2 songs and the fans
def getinitial(inartists):
    #for y in range(0,len(inartists)):
    for y in range(0,10):
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
        tracklist.append(ltrack)
        artistlist.append(lartist)
        #print tracklist
        #print artistlist
        try:
            track=network.get_track(artistlist[len(artistlist)-1],tracklist[len(tracklist)-1])
        except:
            print "Track Error"
        else:
            # Change the number of top fans here - if limit=None, returns 50
                topfans=track.get_top_fans()
                for topfan in topfans:
                    uname=topfan.item.get_name()
                    name=uname.encode('utf-8')
                    userlist.append(name)                                                                                         
    print "Number of users to be crawled: " + len(userlist)
    return True

#get top tracks of fans - returns top 50 tracks
def toptracks():
    for i in range(0,len(userlist)):
        fan=network.get_user(userlist[i])

        # Get banned tracks
        try:
            #print "getting banned tracks for " + userlist[i]
            bannedtracks=fan.get_banned_tracks()
        except:
            print "Could not get banned tracks for " + userlist[i]
        else:
            print len(bannedtracks)
            for bannedtrack in bannedtracks:
                btrack=bannedtrack.track.get_name()
                if not btrack:
                    continue
                print btrack
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
                key=bartist_name+'-'+btrack_name+'-'+userlist[i]
                #print key
                if key not in bannedlist:
                    bannedlist[key]=1
                    writer.writerow([userlist[i],btrack_name,bartist_name,bdate])
                    print len(bannedlist)
    print len(bannedlist)
    return True
            
        



if __name__=="__main__":
    restart = True
    # TODO: put in command-line argument for restart or continue
    if restart:
        print "Getting initial artists"
        inartists=getartist()
        print "Getting initial tracks and users"
        tracklib=getinitial(inartists)
    #tracks=toptracks()
    #fans=topfans()
    try:
        f = open("bannedtracks.csv","r+")
        print "f open"
    except IOError:
        print "Error opening bannedtracks.csv"
        sys.exit(0)
    else:
        writer=csv.writer(f)
        row = [ "user", "banned track","banned track artist","ban date"]
        writer.writerow(row)
        
    for z in range(0,1):     
        print "Getting top tracks"
        tracks=toptracks()


