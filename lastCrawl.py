import pylast

API_KEY = '8b2fa4cb683e168f66f47adcc708ad22'
API_SECRET = '96f5ba11b4313fca6a34b65bba5c5843'
username = 'culturalcluster'
password_hash = pylast.md5("W1nter0zturk")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)

# now you can use that object every where
artist = network.get_artist("System of a Down")
shouts = artist.getShouts()
