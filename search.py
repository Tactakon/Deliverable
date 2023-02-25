import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from dotenv import find_dotenv, load_dotenv
# pip3 install python-dotenv
import os

load_dotenv(find_dotenv())
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))
def search_song(query):
    results = sp.search(q=query, limit=3)
    songs = []
    for idx, track in enumerate(results['tracks']['items']):
        songs.append(track['name'])    #, "by", track['artists'][0]['name']
    return songs                                                    
