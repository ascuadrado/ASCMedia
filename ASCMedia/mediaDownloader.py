import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
import os
import yt_dlp
from youtubesearchpython import VideosSearch
import urllib
import eyed3

# Download options
basePath = "/Users/ascuadrado/Music/Spotify/"

# Client data
sys.path.append("/Users/ascuadrado/Music/Spotify/")
from SpotifyAPI import *

# Login
scope = ["playlist-read-private","playlist-read-private", "playlist-read-collaborative"]
auth_manager=SpotifyOAuth(
  scope=scope,
  client_id = client_id,
  client_secret = client_secret,
  redirect_uri="https://www.freecai.org",
  requests_timeout=5)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Initialize user
user = sp.user(userID)

# Aux functions
def checkIfSongIsDownloaded(name, playlistName):
    fullName = basePath + playlistName + "/" + name + '.mp3'
    return os.path.isfile(fullName)


def getTimeDif(ts, v):
    #print(v)
    timeV = str(v['duration']).split(':')
    timeV = int(timeV[0])*60 + int(timeV[1])

    t_diff = abs(timeV-ts)
    return t_diff

def returnLink(T):
    # Create name for search
    name = ''
    name += (T['track']['name'])
    for artist in T['track']['artists']:
        name += (' ' + artist['name'])

    # Search for video
    videosSearch = VideosSearch(name, limit = 5)
    r = videosSearch.result()

    # Find best time match
    timeS = T['track']['duration_ms']/1000
    bestV = r['result'][0]
    bestTime = getTimeDif(timeS, r['result'][0])

    for v in r['result']:
        if (v['duration'] != None):
            timeV = getTimeDif(timeS, v)
            if (bestTime > timeV):
                bestTime = timeV
                bestV = v
        else:
            pass

    # If there is a big difference (3s), raise alert
    if bestTime > 10:
        print("Big difference: %s (%d s diff)" % (bestV['title'], bestTime))
        #print(bestV)

    return bestV['link']

def download_mp3(T, playlistName):
    path = basePath + playlistName + '/' + T['track']['name']
    ydl_opts = {
        'outtmpl': path + '.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': 'true',
        'no-playlist': 'true'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([returnLink(T)])
    return path + '.mp3'


def addMetadata(T, fileName):
    audiofile = eyed3.load(fileName)

    artists = T['track']['artists']
    audiofile.tag.artist = artists[0]['name']
    if len(artists) > 1:
        for artist in artists[1:]:
            audiofile.tag.artist += ', ' + artist['name']

    audiofile.tag.album = T['track']['album']['name']

    album_artists = T['track']['album']['artists']
    audiofile.tag.album_artist = album_artists[0]['name']
    if len(album_artists) > 1:
        for artist in album_artists[1:]:
            audiofile.tag.artist += ', ' + artist['name']

    audiofile.tag.title = T['track']['name']

    audiofile.tag.track_num = T['track']['track_number']

    audiofile.tag.recording_date = T['track']['album']['release_date'][0:4]

    url = T['track']['album']['images'][0]['url']
    response = urllib.request.urlopen(url)
    imagedata = response.read()
    audiofile.tag.images.set(3, imagedata , "image/jpeg" ,u"Description")

    audiofile.tag.save()


def getPlaylistID(playlist_name):
    playlists = sp.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            if playlist_name == playlist['name']:
                break
        if playlists['next']: # In case there are more than 50
            playlists = sp.next(playlists)
        else:
            playlists = None
    return playlist['id']


def downloadTracksInPlaylist(playlist_ID, playlistName):
    tracks = sp.playlist_items(playlist_ID)
    while tracks:
        for i, track in enumerate(tracks['items']):
            print(track['track']['name'])
            if checkIfSongIsDownloaded(track['track']['name'], playlistName):
                print("(Already downloaded)")
            else:
                file = download_mp3(track, playlistName)
                addMetadata(track, file)
        if tracks['next']: # In case there are more than 100
            tracks = sp.next(tracks)
        else:
            tracks = None
