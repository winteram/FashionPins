# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pylast

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)

# <codecell>

artist = network.get_artist("System of a Down")

# <codecell>

shouts = artist.get_shouts()

# <codecell>

users = {}
for shout in shouts:
    if shout.author not in users:
        users[str(shout.author)] = 1

# <codecell>

hyped = network.get_hyped_artists()

# <codecell>

winteram = network.get_user('winteram')

# <codecell>

print winteram.get_country()

# <codecell>

import urllib2
import json

# <codecell>

toptracks_page = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=8b2fa4cb683e168f66f47adcc708ad22&format=json")

# <codecell>

toptracks = json.loads(toptracks_page.read())

# <codecell>

for track in toptracks['tracks']['track']:
    print "%s by %s" % (track['name'],track['artist']['name'])

# <codecell>

recent = winteram.get_recent_tracks()
