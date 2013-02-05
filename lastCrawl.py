import pylast

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)

# now you can use that object every where
artist = network.get_artist("System of a Down")
# get number of shouts for an artist
shouts = artist.get_shouts(limit=50)

# get listener count of an artist
listenercount=artist.get_listener_count()
# get playcount of an artist
playcount=artist.get_playcount()

# get similar artists to a certain artist
simartists=artist.get_similar()
#for simartist in simartists:
    #print simartist.item.get_name()


# get top tags of a track
track = network.get_track("Billie Holiday", "All of Me")
topItems = track.get_top_tags(limit=None)
#for topItem in topItems:
    #print topItem.item.get_name(), topItem.weight

# get topfans of a track
topfans=track.get_top_fans(limit=None)
#for topfan in topfans:
    #print topfan.item.get_name()
