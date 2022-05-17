import eyed3

audiofile = eyed3.load("Downloads/song.mp3")
audiofile.tag.artist = "Token Entry"
audiofile.tag.album = "Free For All Comp LP"
audiofile.tag.album_artist = "Various Artists"
audiofile.tag.title = "The Edge"
audiofile.tag.track_num = 3

audiofile.tag.save()
