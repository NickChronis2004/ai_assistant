import json
import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
import sensetive_info

scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"

# Authenticate
oauth_object = SpotifyOAuth(client_id=sensetive_info.CLIENT_ID,
                            client_secret=sensetive_info.CLIENT_SECRET,
                            redirect_uri=sensetive_info.REDIRECT_URI,
                            scope=scope)

token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)

def search_and_play_song(song_name):
    try:
        results = spotifyObject.search(song_name, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        if song_items:
            song = song_items[0]['external_urls']['spotify']
            webbrowser.open(song)
            return "Song has opened in your browser."
        else:
            return "No song found with the name: " + song_name
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_user_name():
    user_name = spotifyObject.current_user()
    return user_name['display_name']
