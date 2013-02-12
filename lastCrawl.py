import pylast
import csv

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
def getartist():
    artistlist=artistlist = csv.reader(open("TopArtists.csv", "rb"))
    inartists = []
    for data in artistlist:
        inartists.append(data[0])
    #print inartists
    return inartists

# get initial artists top 2 songs and the fans
def getinitial(inartists):
    for y in range(0,len(inartists)):
        artist = network.get_artist(inartists[y])
        top_tracks=artist.get_top_tracks()
        trackar=[]
        for i in range(0,2):
            for top_track in top_tracks:
                trackar.append(top_track.item.get_name())
                tkey=str(artist)+'-'+trackar[i]
                if tkey not in tracklib:
                    tracklib[tkey]=1
        for item in tracklib:
            lartist=item.split('-')[0]
            ltrack=item.split('-')[1]  
            if type(network.get_track(lartist,ltrack)) == None:
                print "Track Not Found"          
            else:
                track=network.get_track(lartist,ltrack)
                # Change the number of top fans here - if limit=None, returns 50
                topfans=track.get_top_fans(limit=1)
                for topfan in topfans:
                    name=topfan.item.get_name()
                    if name not in fans:
                        fans.append(name)
    print "Number of initial tracks: " +str(len(tracklib))
    print "Number of fans of the initial tracks: " +str(len(fans))
    #print tracklib
    return fans

# get topfans of tracks
def topfans(tracks):
    fans=[]
    for b in range(len(tracks)):
        lartist=tracks[b].split('-')[0]
        ltrack=tracks[b].split('-')[1]  
        
        # Got an error of "Track not found" so thought this might work, it doesn't.
        if type(network.get_track(lartist,ltrack)) == None:
            print "Track Not Found"     
            
        else:
            track=network.get_track(lartist,ltrack)
            #print track
            # Change the number of top fans here - if limit=None, returns 50
            topfans=track.get_top_fans(limit=1)
            for topfan in topfans:
                name=topfan.item.get_name()
                if name not in fans:
                    fans.append(name)
                
    print "Number of fans: " +str(len(fans))
    #print fans
    return fans

#get top tracks of fans - returns top 50 tracks
def toptracks(fans):
    tracks=[]
    for a in range(0,len(fans)):
        fan=network.get_user(fans[a])
        topfantracks=fan.get_top_tracks()
        for topfantrack in topfantracks:
            track=topfantrack.item.get_name()
            track_name=track.encode('utf-8')
            artist=topfantrack.item.get_artist().get_name()
            artist_name=artist.encode('utf-8')
            tracks.append(str(artist_name)+'-'+str(track_name))
            key=unicode(str(artist_name),'utf-8')+'-'+unicode(str(track_name),'utf-8')+'-'+fans[a]
            if key not in fanlib:
                fanlib[key]=1
    print "Number of new tracks: " +str(len(tracks))
    print "Number of fanlib: " +str(len(fanlib))
    return tracks,fanlib


if __name__=="__main__":
    #inartists=getartist()
    inartists=['Maroon 5']
    tracklib=getinitial(inartists)
    for z in range(0,2):     
        tracks,fanlib=toptracks(fans)
        fans=topfans(tracks)
    

