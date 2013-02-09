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

inartists=['Billie Holiday','Charles Aznavour']
# get initial top 100 artists and their top 2 tracks and topfans of those 2 tracks
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
    track=network.get_track(lartist,ltrack)
    topfans=track.get_top_fans(limit=1)
    for topfan in topfans:
        name=topfan.item.get_name()
        if name not in fans:
            fans.append(name)
        

#get top tracks of fans
for a in range(0,len(fans)):
    fan=network.get_user(fans[a])
    topfantracks=fan.get_top_tracks()
    for topfantrack in topfantracks:
        track=topfantrack.item.get_name()
        artist=topfantrack.item.get_artist().get_name()
# I am running to a unicode problem here when trying to concatenate the track name and user name; I've tried unicode and .decode('utf-8')
        key=str(track)+'-'+str(track)+'-'+fans[a]
        print key
        if key not in fanlib:
            fanlib[key]=1


