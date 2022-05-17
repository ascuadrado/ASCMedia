
import os
import yt_dlp
from youtubesearchpython import VideosSearch
import urllib
import eyed3

ydl_opts = {
    'outtmpl': 'Downloads/' + 'StarWars2' + '.%(ext)s',
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
link = 'https://www.youtube.com/watch?v=xlYCxbBZUCY'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])
