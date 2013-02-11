import pylast

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)

tracklib={}
trackar=[]
fans=[]

fanlib={}
inartists=['Etta James']

# get initial top 100 artists and their top 2 tracks
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
    print "Number of initial tracks: " +str(len(tracklib))
    print tracklib
    return tracklib

# get topfans of tracks
def topfans(tracklib):
    fans=[]
    for item in tracklib:
        lartist=item.split('-')[0]
        ltrack=item.split('-')[1]
        # Got an error of "Track not found" so thought this might work
        try:
            track=network.get_track(lartist,ltrack)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'Something.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Something else.'
                print 'Error code: ', e.code
        else:
            # Change the number of top fans here - if limit=None, returns 50
            topfans=track.get_top_fans(limit=3)
            for topfan in topfans:
                name=topfan.item.get_name()
                if name not in fans:
                    fans.append(name)
        print "Number of fans: " +str(len(fans))
        print fans
        return fans

#get top tracks of fans - returns top 50 tracks
def toptracks(fans):
    for a in range(0,len(fans)):
        fan=network.get_user(fans[a])
        topfantracks=fan.get_top_tracks()
        for topfantrack in topfantracks:
            track=topfantrack.item.get_name()
            track_name=track.encode('utf-8')
            artist=topfantrack.item.get_artist().get_name()
            artist_name=artist.encode('utf-8')
            key=unicode(str(artist_name),'utf-8')+'-'+unicode(str(track_name),'utf-8')+'-'+fans[a]
            if key not in fanlib:
                fanlib[key]=1
    print "Number of toptracks: " +str(len(fanlib))
    return fanlib


if __name__=="__main__":
    tracklib=getinitial(inartists)
    fans=topfans(tracklib)
    for z in range(0,3):     
        fanlib=toptracks(fans)
        fans=topfans(fanlib)
    

