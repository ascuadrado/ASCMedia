import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


auth_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

user = sp.user(userID)
p = sp.user_playlists(userID)
t = sp.playlist_items(p['items'][0]['id'])
sp.audio_analysis(t['items'][0]['track']['id'])

t
