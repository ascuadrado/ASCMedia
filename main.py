from ASCMedia import mediaDownloader
import sys

if __name__ == '__main__':
    # Log in
    # Ask for playlist name
    # Find playlist id
    # Get track data
    # Find in youutbe
    # Download
    # Insert metadata
    if(len(sys.argv) > 1):
        playlistName = sys.argv[1]
        print(playlistName)

    playlistID = mediaDownloader.getPlaylistID(playlistName)
    mediaDownloader.downloadTracksInPlaylist(playlistID, playlistName)

# END
