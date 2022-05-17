
# %% Imports

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from youtubesearchpython import VideosSearch
import youtube_dl
import urllib
import eyed3

# %% Playlist name, etc


# %% Auxiliary functions

def getTimeDif(ts, v):
    timeV = v['duration'].split(':')
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
        timeV = getTimeDif(timeS, v)
        if (bestTime > timeV):
            bestTime = timeV
            bestV = v

    # If there is a big difference (3s), raise alert
    if bestTime > 10:
        print("Big difference: %s %d" % (name, bestTime))

    return bestV['link']


def download_mp3(T):
    ydl_opts = {
        'outtmpl': 'Downloads/' + T['track']['name'] + '.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([returnLink(T)])
    return 'Downloads/' + T['track']['name'] + '.mp3'


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

# %% Authentication

auth_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# %% Get playlist

user = sp.user(userID)

playlists = sp.user_playlists(user = userID)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlist_name in playlist['name']:
            break
    if playlists['next']: # In case there are more than 50
        playlists = sp.next(playlists)
    else:
        playlists = None

playlist_id = playlist['id']

# %% Get tracks

tracks = sp.playlist_items(playlist_id)
while tracks:
    for i, track in enumerate(tracks['items']):
        print(track['track']['name'])
        file = download_mp3(track)
        addMetadata(track, file)
    if tracks['next']: # In case there are more than 100
        tracks = sp.next(tracks)
    else:
        tracks = None

# %% Testing new features
T = tracks['items'][1]
T['track']['name']

file = download_mp3(T)

import yt_dlp

def download_mp3(T):
    ydl_opts = {
        'outtmpl': 'Downloads/' + T['track']['name'] + '.%(ext)s',
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([returnLink(T)])
    return 'Downloads/' + T['track']['name'] + '.mp3'
